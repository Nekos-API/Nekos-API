export default async function handler(req, res) {
    const response = await fetch(
        process.env.NEXT_PUBLIC_API_BASE +
            "/auth/external/discord?code=" +
            encodeURIComponent(req.query.code),
        {
            method: "GET",
            headers: {
                Authorization: "Token " + process.env.PROTECTED_API_TOKEN,
                "Content-Type": "application/vnd.api+json",
            },
        }
    );

    const data = await response.json();

    res.status(200).redirect(
        `/login?access_token=${encodeURIComponent(
            data.data.attributes.access_token
        )}&refresh_token=${encodeURIComponent(
            data.data.attributes.refresh_token
        )}`
    );
}
