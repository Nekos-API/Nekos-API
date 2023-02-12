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

    useUser() {
        const { user, setUser, isLoading, setIsLoading, error, setError } =
            React.useContext(AuthContext).user;

        const handler = () => {
            if (!isLoading) {
                setIsLoading(true);
                fetch(process.env.NEXT_PUBLIC_API_BASE + "/users/@me", {
                    credentials: 'include',
                    headers: {
                        Accept: "application/vnd.api+json",
                    },
                })
                    .catch((err) => {
                        setError(err);
                        setIsLoading(false);
                    })
                    .then((data) => data.json())
                    .then((data) => {
                        if (data.errors) {
                            if (data.errors[0].code != "not_authenticated") {
                                setError(data.errors[0].code)
                            }
                            setIsLoading(false);
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
