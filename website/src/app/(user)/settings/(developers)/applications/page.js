"use client";

import { ExclamationCircleIcon } from "@heroicons/react/24/outline";

import useSWR from "swr";
import React from "react";
import { LightPrimaryButton } from "@/components/button";
import Link from "next/link";

const fetcher = async (url) => {
    const res = await fetch(process.env.NEXT_PUBLIC_API_BASE + url, {
        credentials: "include",
        headers: {
            Accept: "application/vnd.api+json",
        },
    });
    return await res.json();
};

export default function Applications() {
    const { data, isLoading, error } = useSWR("/applications", fetcher);

    return (
        <div className="flex flex-col gap-6 text-sm relative">
            <h2 className="text-3xl font-extrabold">Applications</h2>
            <div className="flex flex-row gap-4 p-4 rounded-lg border-2 border-neutral-200 bg-neutral-100">
                <ExclamationCircleIcon className="h-6 w-6" />
                <div className="flex flex-col gap-2 flex-1">
                    <div className="font-bold text-base">Warning</div>
                    <p>
                        Store your client secret when you create an application.
                        You will not see it again.
                    </p>
                </div>
            </div>
            <div className="flex flex-row gap-4 p-4 rounded-lg border-2 border-neutral-200 bg-neutral-100">
                <ExclamationCircleIcon className="h-6 w-6" />
                <div className="flex flex-col gap-2 flex-1">
                    <div className="font-bold text-base">Info</div>
                    <p>
                        This GUI is a disaster. It is much easier to create,
                        edit and delete applications using the API than managing
                        them from here.
                    </p>
                </div>
            </div>
            <div className="flex flex-row items-center justify-between w-full mt-6">
                <div className="text-xl font-extrabold">My applications</div>
                <Link href="/settings/applications/create">
                    <LightPrimaryButton>
                        Create new application
                    </LightPrimaryButton>
                </Link>
            </div>
            <div className="grid md:grid-cols-2 gap-6 w-full relative">
                {isLoading ? (
                    <>Loading...</>
                ) : error ? (
                    <>Error</>
                ) : (
                    data.data.map((value, index) => {
                        return (
                            <Application
                                icon={value.attributes.icon}
                                name={value.attributes.name}
                                description={value.attributes.description}
                                credentials={value.attributes.credentials}
                                authorizationGrantType={
                                    value.attributes.authorizationGrantType
                                }
                                redirectUris={value.attributes.redirectUris}
                                clientType={value.attributes.clientType}
                            />
                        );
                    })
                )}
            </div>
        </div>
    );
}

function Application({
    icon,
    banner,
    name,
    description,
    credentials: { clientId, clientSecret } = {},
    authorizationGrantType,
    clientType,
    redirectUris,
}) {
    return (
        <div className="w-full rounded-lg overflow-hidden bg-white dark:bg-neutral-900 relative border dark:border-0 border-neutral-200 drop-shadow-md">
            {banner ? (
                <div className="bg-neutral-700 h-32">
                    <img src={banner} className="h-32 w-full object-cover" />
                </div>
            ) : (
                <div
                    className="h-32 bg-neutral-100 dark:bg-neutral-800"
                    style={{
                        background: `radial-gradient(#fe5c51 0.5px, transparent 0.5px), radial-gradient(#fe5c51 0.5px, transparent 0.5px)`,
                        backgroundSize: "20px 20px",
                        backgroundPosition: "0 0,10px 10px",
                    }}
                ></div>
            )}
            <div className="relative p-4">
                <div className="bg-neutral-200 dark:bg-black -mt-12 rounded-2xl border-[6px] border-neutral-200 dark:border-black overflow-hidden w-fit aspect-square flex flex-col items-center justify-center text-center">
                    {icon ? (
                        <img src={icon} className="h-12 w-12 object-cover" />
                    ) : (
                        <div className="text-xl h-12 w-12 text-center flex flex-col items-center justify-center">
                            {name.substring(0, 2)}
                        </div>
                    )}
                </div>
                <div className="my-4">
                    <div className="font-medium text-xl leading-none text-neutral-900 dark:text-neutral-100">
                        {name}
                    </div>
                    <div className="mt-2 text-sm text-neutral-600 dark:text-neutral-400 line-clamp-3">
                        {description}
                    </div>
                    <div className="mt-4 flex flex-col gap-4">
                        <div>
                            <div className="font-extrabold">Client ID</div>
                            <div className="break-all text-xs">{clientId}</div>
                        </div>
                        <div>
                            <div className="font-extrabold">Client Secret</div>
                            <div className="break-all text-xs">
                                {clientSecret ? clientSecret : "Hidden"}
                            </div>
                        </div>
                        <div>
                            <div className="font-extrabold">
                                Authorization Grant Type
                            </div>
                            <div className="break-all text-xs">
                                {authorizationGrantType == "password"
                                    ? "Resource owner username password"
                                    : authorizationGrantType ==
                                      "authorization-code"
                                    ? "Authorization code"
                                    : authorizationGrantType == "implicit"
                                    ? "Implicit"
                                    : authorizationGrantType ==
                                      "client_credentials"
                                    ? "Client credentials"
                                    : "OpenID connect hybrid"}
                            </div>
                        </div>
                        <div>
                            <div className="font-extrabold">Client type</div>
                            <div className="break-all text-xs">
                                {clientType == "confidential"
                                    ? "Confidential"
                                    : "Public"}
                            </div>
                        </div>
                        <div>
                            <div className="font-extrabold">Redirect URIs</div>
                            <div className="break-all text-xs">
                                {redirectUris.split(" ").map((value, index) => {
                                    return (
                                        <>
                                            {value}
                                            <br />
                                        </>
                                    );
                                })}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
