"use client";

import Auth from "@/utils/authorization";
import { useRouter, useSearchParams } from "next/navigation";
import React from "react";

/**
 * The only purpose of this link is to redirect to the authorization page in
 * the API. This is needed because, as auth credentials are stored in
 * `localStorage` they are not available in the `api.nekosapi.com` domain and
 * therefore redirecting users there directly would require them to re-login.
 *
 * This function redirects to the authorization page and sends all the query
 * params sent to this view to the `api.nekosapi.com/v2/auth/authorize` url,
 * together with the `access_token` param for authentication.
 *
 * @returns <></>;
 */
export default function Authorize() {
    const router = useRouter();
    const params = useSearchParams();

    const auth = new Auth();

    const { user, isLoading, error } = auth.useUser();

    React.useEffect(() => {
        if (user) {
            const { access_token: accessToken } = auth.getSession();

            const url = new URL(
                "/v2/auth/authorize",
                process.env.NEXT_PUBLIC_API_BASE
            );
            
            for (let [name, value] of params) {
                url.searchParams.append(name, value);
            }

            url.searchParams.append("access_token", accessToken);

            // Replace is used because as this redirects to the `api.nekosapi.com`
            // domain this should not be added to history (i.e. ignored when go
            // back is pressed)
            window.location.href = url.toString();
        } else if (auth.getSession() == null) {
            // If the user is null and is not loading, then the user has not
            // logged in yet. 
            router.replace("/login");
        }
    }, [user]);

    return (
        <div className="h-full w-full flex flex-col items-center justify-center">
            <div className="h-6 w-6 border-2 border-crayola-350 border-t-transparent rounded-full animate-spin"></div>
        </div>
    );
}
