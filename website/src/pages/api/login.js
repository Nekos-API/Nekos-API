import * as requestIp from "request-ip";
import { FormData } from 'node-fetch';

export default async function handler(req, res) {
    if (req.method !== "POST") {
        res.status(405).send({ message: "Only POST requests allowed" });
        return;
    }

    const capcha_response = await fetch(
        `https://www.google.com/recaptcha/api/siteverify?secret=${encodeURIComponent(
            process.env.RECAPTCHA_SITE_SECRET
        )}&response=${encodeURIComponent(
            req.body.token
        )}&remoteip=${encodeURIComponent(requestIp.getClientIp(req))}`,
        {
            method: "POST",
        }
    );
    const captcha_json = await capcha_response.json();

    if (captcha_json.score < 0.6) {
        res.status(403).json({
            success: false,
            data: {
                message: "Could not verify reCAPTCHA. Are you a bot?",
            },
        });
        return;
    }

    fetch(process.env.NEXT_PUBLIC_API_BASE + "/auth/token", {
        method: "POST",
        headers: {
            Authorization:
                "Basic " +
                Buffer.from(
                    process.env.APPLICATION_CLIENT_ID +
                        ":" +
                        process.env.APPLICATION_CLIENT_SECRET
                ).toString("base64"),
            "Content-Type": "application/json",
            Accept: "application/vnd.api+json"
        },
        body: JSON.stringify({
            "grant_type": "password",
            "username": req.body.username,
            "password": req.body.password
        }),
    })
        .catch((reason) => {
            res.status(500).json({
                success: false,
                data: {
                    message: "An unknown error ocurred.",
                },
            });
        })
        .then((data) => data.json())
        .then((data) => {
            if (data.error === undefined) {
                res.status(200).json({
                    success: true,
                    data,
                });
            } else if (data.error === "invalid_grant") {
                res.status(401).json({
                    success: false,
                    data: {
                        message: "The username and password do not match."
                    },
                });
            } else {
                res.status(500).json({
                    success: false,
                    data: {
                        message: "An unknown error ocurred.",
                    },
                });
            }
        });
}
