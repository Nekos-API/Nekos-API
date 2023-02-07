import React from "react";

import { AuthContext } from "@/app/layout";

export default class Auth {
    constructor(authContext = React.useContext(AuthContext)) {
        this._update = authContext.v;
        this._setUpdate = authContext.sv;
        this.setUser = authContext.user.setUser
        this.setError = authContext.user.setError
        this.setIsLoading = authContext.user.setIsLoading
    }

    update() {
        this._setUpdate(!this._update);
    }

    getSession() {
        return localStorage.getItem("auth")
            ? JSON.parse(localStorage.getItem("auth"))
            : null;
    }

    setSession({ access_token, refresh_token }) {
        localStorage.setItem(
            "auth",
            JSON.stringify({
                access_token,
                refresh_token,
            })
        );
    }

    /**
     *
     * @param {*} username The user's username
     * @param {*} password The user's plain password
     * @param {*} token The recaptcha token
     * @returns `[success, errorMessage]`
     */
    async login(username, password, token) {
        const res = await fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username,
                password,
                token,
            }),
        });
        const json = await res.json();

        if (json.success) {
            this.setSession({
                access_token: json.data.access_token,
                refresh_token: json.data.refresh_token,
            });
            this.update();
            return [true, null];
        } else {
            return [false, json.data.message];
        }
    }

    logout() {
        localStorage.removeItem("auth");
        this.setUser(null);
        this.setError(null);
        this.update();
    }

    async refresh() {
        await fetch("/api/refresh", {
            method: "POST",
            body: JSON.stringify({
                refresh_token: this.getSession().refresh_token,
            }),
        })
            .then((data) => data.json())
            .then((data) => {
                if (data.access_token) {
                    this.setSession({
                        access_token: data.access_token,
                        refresh_token: this.getSession().refresh_token,
                    });
                }
            });
    }

    useUser() {
        const { user, setUser, isLoading, setIsLoading, error, setError } =
            React.useContext(AuthContext).user;

        const handler = () => {
            if (localStorage.getItem("auth") != null && !isLoading && user == undefined) {
                setIsLoading(true);
                fetch(process.env.NEXT_PUBLIC_API_BASE + "/users/@me", {
                    headers: {
                        Accept: "application/vnd.api+json",
                        Authorization:
                            "Bearer " + this.getSession().access_token,
                    },
                })
                    .catch((err) => {
                        setError(err);
                        setIsLoading(false);
                    })
                    .then((data) => data.json())
                    .then((data) => {
                        if (data.errors) {
                            if (data.errors[0].code == "not_authenticated") {
                                this.refresh()
                                    .catch((err) => {
                                        setError(err);
                                        setIsLoading(false);
                                    })
                                    .then(() => {
                                        fetch(
                                            process.env.NEXT_PUBLIC_API_BASE +
                                                "/users/@me",
                                            {
                                                headers: {
                                                    Accept: "application/vnd.api+json",
                                                    Authorization:
                                                        "Bearer " +
                                                        this.getSession()
                                                            .access_token,
                                                },
                                            }
                                        )
                                            .catch((err) => {
                                                setError(err);
                                                setIsLoading(false)
                                            })
                                            .then((data) => data.json())
                                            .then((data) => {
                                                setUser(data.data);
                                                setIsLoading(false);
                                            });
                                    });
                            }
                        } else {
                            setUser(data.data);
                            setIsLoading(false);
                        }
                    });
            }
        };

        React.useEffect(handler, []);
        React.useEffect(handler, [this._update]);

        return {
            user,
            error,
            isLoading,
        };
    }
}
