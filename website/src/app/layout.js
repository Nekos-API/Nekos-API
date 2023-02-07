"use client";

import React from "react";
import Navbar from "@/components/navbar";
import "./globals.css";

export const AuthContext = React.createContext({
    v: false,
    sv: null,
    user: {
        user: null,
        setUser: null,
        isLoading: null,
        setIsLoading: null,
        error: null,
        setError: null,
    },
});

export default function RootLayout({ children }) {
    const [v, sv] = React.useState(false);
    const [user, setUser] = React.useState(null);
    const [error, setError] = React.useState(null);
    const [isLoading, setIsLoading] = React.useState(false);

    return (
        <AuthContext.Provider
            value={{
                v,
                sv,
                user: {
                    user,
                    setUser,
                    isLoading,
                    setIsLoading,
                    error,
                    setError
                }
            }}
        >
            <html lang="en">
                <head />
                <body className="overflow-y-scroll">
                    <Navbar />
                    <div className="flex flex-col items-center p-4">
                        <div className="flex w-full max-w-5xl">{children}</div>
                    </div>
                </body>
            </html>
        </AuthContext.Provider>
    );
}
