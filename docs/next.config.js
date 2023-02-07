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
        ];
    },
});
