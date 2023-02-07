export default function handler(req, res) {
    res.redirect(
        "https://discord.com/api/oauth2/authorize?client_id=1070539872084951050&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fapi%2Fauth%2Fdiscord%2Fcallback&response_type=code&scope=identify%20email"
    );
}
