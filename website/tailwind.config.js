/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/**/*.{js,ts,jsx,tsx}"],
    theme: {
        extend: {
            colors: {
                crayola: {
                    50: "#fff2f2",
                    100: "#ffe4e3",
                    150: "#ffc0bc",
                    200: "#ffafaa",
                    250: "#fe8e87",
                    300: "#fe7a72",
                    350: "#fe5c51",
                    400: "#fe453a",
                    450: "#fe2a1c",
                    500: "#fe1001",
                    550: "#e30f01",
                    600: "#c50d01",
                    650: "#ad0b01",
                    700: "#8d0901",
                    750: "#780801",
                    800: "#540500",
                    850: "#430400",
                    900: "#1c0200",
                    950: "#0d0100",
                },
                tufts: {
                    100: "#e6f1fc",
                    200: "#b4d4f5",
                    300: "#81b8ef",
                    400: "#4f9ce8",
                    500: "#1d7fe2",
                    600: "#1763b0",
                    700: "#10477e",
                    800: "#0a2a4b",
                    900: "#030e19",
                },
                spring: {
                    100: "#e4feef",
                    200: "#adfcd0",
                    300: "#77f9b1",
                    400: "#41f792",
                    500: "#0af573",
                    600: "#08be59",
                    700: "#068840",
                    800: "#035226",
                    900: "#011b0d",
                },
            },
        },
        fontFamily: {
            nunito: ["'Nunito'", "sans-serif"],
        },
    },
    plugins: [
        require("@tailwindcss/line-clamp"),
        // ...
    ],
};
