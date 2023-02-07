export default async function handler(req, res) {
    if (req.method !== "POST") {
        res.status(405).send({ message: "Only POST requests allowed" });
        return;
    }

    try {
        const response = await fetch(
            process.env.NEXT_PUBLIC_API_BASE + "/auth/token",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "grant_type": "refresh_token",
                    "refresh_token": JSON.parse(req.body).refresh_token,
                    "client_id": process.env.APPLICATION_CLIENT_ID,
                    "client_secret": process.env.APPLICATION_CLIENT_SECRET
                }),
            }
        );
        const data = await response.json();

        if (data.error === undefined) {
            res.status(200).json({
                success: true,
                data,
            });
        } else {
            res.status(500).json({
                success: false,
                data: {
                    message: "An unknown error ocurred.",
                    error: data.error,
                    body: {
                        "grant_type": "refresh_token",
                        "refresh_token": JSON.parse(req.body).refresh_token,
                        "client_id": process.env.APPLICATION_CLIENT_ID,
                        "client_secret": process.env.APPLICATION_CLIENT_SECRET
                    }
                },
            });
        }
    } catch (e) {
        console.log(e);
        res.status(500).json({
            success: false,
            data: {
                message: "An unknown error ocurred.",
            },
        });
    }
}
