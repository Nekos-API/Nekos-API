"use client";

import React from "react";

import { ScaleBorderButton, ScalePrimaryButton } from "@/components/button";
import { UserIcon, LockClosedIcon } from "@heroicons/react/24/outline";
import Link from "next/link";
import Script from "next/script";
import Auth from "@/utils/authorization";
import { useRouter, useSearchParams } from "next/navigation";

export default function Login() {
    const usernameRef = React.useRef();
    const passwordRef = React.useRef();
    
    const router = useRouter();
    
    const auth = new Auth();

    const [isAuthLoading, setIsAuthLoading] = React.useState(false);

    const searchParams = useSearchParams();

    React.useEffect(() => {
        if (searchParams.get('access_token') && searchParams.get('refresh_token')) {
            auth.setSession({
                access_token: searchParams.get('access_token'),
                refresh_token: searchParams.get('refresh_token')
            })
            auth.update()
            setIsAuthLoading(true);
            router.replace('/');
        }
    }, [])

    return (
        <div className="flex flex-col items-center justify-center w-full">
            <form
                className="my-8 w-full max-w-xs relative"
                onSubmit={(e) => {
                    e.preventDefault();
                    setIsAuthLoading(true);
                    grecaptcha.ready(function () {
                        grecaptcha
                            .execute(
                                process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY,
                                {
                                    action: "submit",
                                }
                            )
                            .then(function (token) {
                                auth.login(
                                    usernameRef.current.value,
                                    passwordRef.current.value,
                                    token
                                ).then((data) => {
                                    const [success, errorMessage] = data;
                                    if (success) {
                                        console.log("Logged in!");
                                        router.push("/");
                                    } else {
                                        alert(errorMessage);
                                    }
                                    setIsAuthLoading(false);
                                });
                            });
                    });
                }}
            >
                <h2 className="text-3xl font-extrabold">Log in</h2>
                <p className="text-neutral-500">Catgirls are cute, right?</p>
                <div className="mt-4 flex flex-col gap-4">
                    <div className="relative w-full">
                        <input
                            className="p-2 pl-8 leading-none rounded-lg bg-transparent w-full z-10 block relative outline-none peer placeholder:text-neutral-400 font-medium"
                            placeholder="Username"
                            required={true}
                            name="username"
                            ref={usernameRef}
                        />
                        <div className="absolute top-0 bottom-0 left-0 right-0 rounded-lg transition-all bg-neutral-100 peer-focus:scale-x-[1.025] peer-focus:scale-y-105"></div>
                        <UserIcon className="h-5 w-5 absolute top-0 bottom-0 left-2 my-auto" />
                    </div>
                    <div className="relative w-full">
                        <input
                            className="p-2 pl-8 leading-none rounded-lg bg-transparent w-full z-10 block relative outline-none peer placeholder:text-neutral-400 font-medium"
                            placeholder="Password"
                            required={true}
                            type="password"
                            name="password"
                            ref={passwordRef}
                        />
                        <div className="absolute top-0 bottom-0 left-0 right-0 rounded-lg transition-all bg-neutral-100 peer-focus:scale-x-[1.025] peer-focus:scale-y-105"></div>
                        <LockClosedIcon className="h-5 w-5 absolute top-0 bottom-0 left-2 my-auto" />
                    </div>
                    <Link
                        href="/password-reset"
                        className="flex flex-row items-center gap-2 text-crayola-350 -mt-2 underline decoration-crayola-150 hover:decoration-crayola-300 transition-colors underline-offset-4 text-sm"
                    >
                        Forgot your passsword?
                    </Link>
                </div>
                <div className="flex flex-col gap-4 mt-8">
                    <div className="w-full grid grid-cols-2 items-center gap-4">
                        <ScalePrimaryButton>
                            <div
                                className="transition-all"
                                style={{
                                    opacity: isAuthLoading ? "0" : "1",
                                }}
                            >
                                Log in
                            </div>
                            <div
                                className="h-5 w-5 rounded-full border-2 border-white border-t-transparent animate-spin absolute top-0 bottom-0 left-0 right-0 transition-all m-auto"
                                style={{
                                    opacity: isAuthLoading ? "1" : "0",
                                }}
                            ></div>
                        </ScalePrimaryButton>
                        <Link href="/signup" className="flex-1 flex flex-row">
                            <ScaleBorderButton>Sign up</ScaleBorderButton>
                        </Link>
                    </div>
                    <div className="flex flex-row items-center gap-2 w-full">
                        <div className="h-0.5 rounded-full bg-neutral-200 flex-1"></div>
                        <div className="uppercase text-xs leading-none text-neutral-400">
                            or
                        </div>
                        <div className="h-0.5 rounded-full bg-neutral-200 flex-1"></div>
                    </div>
                    <div className="w-full grid grid-cols-3 items-center gap-4">
                        <a href="/api/auth/discord" className="w-full flex flex-row">
                            <ScaleBorderButton type="button">
                                <img src="/logos/discord.svg" className="h-5 w-5" />
                            </ScaleBorderButton>
                        </a>
                        <ScaleBorderButton type="button">
                            <img src="/logos/google.svg" className="h-5 w-5" />
                        </ScaleBorderButton>
                        <ScaleBorderButton type="button">
                            <img src="/logos/github.svg" className="h-5 w-5" />
                        </ScaleBorderButton>
                    </div>
                </div>
            </form>
            <Script
                src={`https://www.google.com/recaptcha/api.js?render=${process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY}`}
            />
        </div>
    );
}
