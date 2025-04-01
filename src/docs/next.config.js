// next.config.js
const withNextra = require("nextra")({
    theme: "nextra-theme-docs",
    themeConfig: "./theme.config.jsx",
    defaultShowCopyCode: true,
    // optional: add `unstable_staticImage: true` to enable Nextra's auto image import
});
module.exports = withNextra({
    images: {
        loader: "akamai",
        path: "/",
        domains: ["discordapp.com"],
    },
    trailingSlash: false,
    async headers() {
        return [
            {
                source: "/:path(!api)",
                headers: [
                    {
                        key: "Content-Security-Policy",
                        value: `default-src 'none'; script-src 'self'; connect-src 'self'; img-src 'self' ${process.env.NEXT_PUBLIC_SUPABASE_URL}; style-src 'self';base-uri 'self';form-action 'self'`,
                    },
                ],
            },
            {
                source: "/api/:path*",
                headers: [
                    { key: "Access-Control-Allow-Credentials", value: "true" },
                    { key: "Access-Control-Allow-Origin", value: "*" }, // replace this your actual origin
                    { key: "Access-Control-Allow-Methods", value: "GET,DELETE,PATCH,POST,PUT" },
                    { key: "Access-Control-Allow-Headers", value: "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version" },
                ]
            }
        ];
    },
});
