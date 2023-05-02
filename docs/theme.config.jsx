import React from "react"
import { useRouter } from "next/router"
import { useConfig } from "nextra-theme-docs"
import { UserCircleIcon } from "@heroicons/react/24/outline"
import useSWR from "swr"

import Link from "next/link"
import Script from "next/script"

import Popup from "./src/components/popup"

const userFetcher = (url) => fetch(`${process.env.NEXT_PUBLIC_API_BASE}${url}`, {
    credentials: "include",
    headers: {
        Accept: "application/vnd.api+json"
    }
}).then(res => res.json())

const useUser = () => {
    const { data, error, isLoading } = useSWR("/v2/users/@me", userFetcher)

    return {
        user: data,
        error,
        isLoading
    }
}

const statusFetcher = () => fetch('/api/status', { cache: "no-store" }).then(res => res.json())
const useStatus = () => {
    const { data, error, isLoading } = useSWR(statusFetcher)

    return {
        status: data,
        error,
        isLoading
    }
}

export default {
    logo: () => {
        return (
            <div style={{ display: "flex", flexDirection: "row", alignItems: "center", gap: "1rem" }}>
                <img src="/branding/logo/logo.png" alt="Logo" width={32} height={32} />
                <span>Nekos API</span>
            </div>
        )
    },
    project: {
        link: 'https://github.com/Nekos-API/Nekos-API',
    },
    docsRepositoryBase: "https://github.com/Nekidev/Nekos-API/tree/main",
    useNextSeoProps() {
        const { route } = useRouter()
        if (route !== '/') {
            return {
                titleTemplate: '%s – Nekos API'
            }
        } else {
            return {
                titleTemplate: 'Nekos API - The open-source anime images API'
            }
        }
    },
    head: () => {
        const { asPath } = useRouter()
        const { frontMatter } = useConfig()
        return <>
            <meta property="og:type" content="website" />
            <meta property="og:url" content={`https://nekosapi.com${asPath}`} />
            <meta property="og:title" content={frontMatter.title || 'Nekos API Documentation'} />
            <meta property="og:description" content={frontMatter.description || 'The open-source free public anime images Restful API. Get +10k manually added and verified high quality anime images with metadata such as the artist, original post, categories, characters, and even color palette using a single API!'} />
            <meta property="og:image" content="/branding/banner.png" />

            <meta name="description" content={frontMatter.description || 'The open-source free public anime images Restful API. Get +10k manually added and verified high quality anime images with metadata such as the artist, original post, categories, characters, and even color palette using a single API!'} />
            <meta name="theme-color" content="#ff0055" />

            <meta property="twitter:card" content="summary_large_image" />
            <meta property="twitter:url" content="https://nekosapi.com/" />
            <meta property="twitter:title" content="Nekos API" />
            <meta property="twitter:description" content="The open-source free public anime images Restful API. Get +10k manually added and verified high quality anime images with metadata such as the artist, original post, categories, characters, and even color palette using a single API!" />
            <meta property="twitter:image" content="/branding/banner.png" />
        </>
    },
    primaryHue: {
        light: 350,
        dark: 340,
    },
    chat: {
        "link": "https://discord.gg/b9Fv3kEfXc"
    },
    banner: {
        "key": "WebSockets-API-released",
        "text": (
            <Link href="/docs/websockets" style={{ display: "flex", flexDirection: "row", alignItems: "center", justifyContent: "center", gap: ".5rem" }}>
                ✨ <span className="font-mono">WebSockets API</span> is live! Click on this banner to learn more ✨
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" style={{ height: "1rem", width: "1rem" }}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                </svg>
            </Link>
        )
    },
    footer: {
        text: () => {
            const { status, error, isLoading } = useStatus();

            return (
                <div className="flex flex-col md:flex-row items-center justify-between w-full gap-4">
                    <div>
                        MIT {new Date().getFullYear()} © <a href="https://nekidev.com" target="_blank">Nekidev</a>. Made with ❤ from Argentina.
                    </div>
                    <Link href="https://status.nekosapi.com/" target="_blank" className="rounded p-2 border border-neutral-200 hover:border-neutral-400 dark:border-neutral-800 dark:hover:border-neutral-600 bg-white dark:bg-black leading-none w-fit text-neutral-800 dark:text-white font-medium flex flex-row items-center gap-2 drop-shadow-sm transition cursor-pointer">
                        {isLoading ? (
                            <>
                                <div className="h-2.5 w-2.5 rounded-full bg-neutral-400">
                                    <div className="h-2.5 w-2.5 rounded-full bg-neutral-400 animate-ping"></div>
                                </div>
                                Status:
                                <span>
                                    Loading...
                                </span>
                            </>
                        ) : error || (status != null && status.status != "up") ? (
                            <>
                                <div className="h-2.5 w-2.5 rounded-full bg-red-400">
                                    <div className="h-2.5 w-2.5 rounded-full bg-red-400 animate-ping"></div>
                                </div>
                                Status:
                                <span className="text-red-400">
                                    Some systems are down!
                                </span>
                            </>
                        ) : (
                            <>
                                <div className="h-2.5 w-2.5 rounded-full bg-green-400">
                                    <div className="h-2.5 w-2.5 rounded-full bg-green-400 animate-ping"></div>
                                </div>
                                Status:
                                <span className="text-green-400">
                                    All systems are up
                                </span>
                            </>
                        )}
                        
                    </Link>
                </div>
            )
        }
    },
    navbar: {
        extraContent: () => {
            const { user, error, isLoading } = useUser()

            if (isLoading) return <div className="ml-2 m-0.5 h-6 w-6 rounded-full border-2 border-[hsl(var(--nextra-primary-hue),100%,50%)] border-t-transparent animate-spin"></div>
            if (error || (user && "errors" in user)) {
                return (
                    <Popup
                        trigger={(
                            <UserCircleIcon className="h-7 w-7" />
                        )}
                        triggerContainerClassName="ml-1.5 flex flex-col items-center justify-center w-7 h-7 cursor-pointer"
                        alignment="bottom-right"
                        popupContainerClassName="pt-3"
                        initialAnim={{
                            y: -5,
                            opacity: 0
                        }}
                        animate={{
                            y: 0,
                            opacity: 1,
                            transition: {
                                duration: .1
                            }
                        }}
                        exitAnim={{
                            y: -5,
                            opacity: 0,
                            transition: {
                                duration: .1
                            }
                        }}
                    >
                        <div className="py-1 border border-neutral-700 rounded-lg bg-neutral-800 drop-shadow whitespace-nowrap flex flex-col">
                            <Link href={process.env.NEXT_PUBLIC_NEKOS_API_AUTH_URL} className="nx-relative nx-hidden nx-w-full nx-select-none nx-whitespace-nowrap nx-text-gray-600 hover:nx-text-gray-900 dark:nx-text-gray-400 dark:hover:nx-text-gray-100 md:nx-inline-block nx-py-1.5 nx-transition-colors ltr:nx-pl-3 ltr:nx-pr-9 rtl:nx-pr-3 rtl:nx-pl-9">Log in</Link>
                            <Link href="" className="nx-relative nx-hidden nx-w-full nx-select-none nx-whitespace-nowrap nx-text-gray-600 hover:nx-text-gray-900 dark:nx-text-gray-400 dark:hover:nx-text-gray-100 md:nx-inline-block nx-py-1.5 nx-transition-colors ltr:nx-pl-3 ltr:nx-pr-9 rtl:nx-pr-3 rtl:nx-pl-9">Sign up</Link>
                        </div>
                    </Popup>
                )
            }

            return <div className="ml-1.5 min-w-7">
                <img src={user.data.attributes.avatarImage} className="rounded-full object-cover h-7 w-7" />
            </div>
        }
    },
    sidebar: {
        defaultMenuCollapseLevel: 1,
        toggleButton: true,
    },
    toc: {
        extraContent: () => {
            return (
                <>
                    <Script async={true} src="https://media.ethicalads.io/media/client/ethicalads.min.js" />
                    <div id="ad-docs-toc-main">
                        <div className="bordered" data-ea-publisher="nekosapicom" id="ad-docs-toc"></div>
                    </div>
                    <Script>{`
                        const ad_container_main = document.getElementById("ad-docs-toc-main");
                        const ad_container_alt = document.getElementById("ad-docs-toc-alt");
                        const ad_element = document.getElementById("ad-docs-toc");

                        function setAdTheme() {
                            if (document.documentElement.className.includes("dark")) {
                                ad_element.classList.add("dark");
                            } else {
                                ad_element.classList.remove("dark");
                            }
                        };

                        function callback(mutationList, observer) {
                            mutationList.forEach(function(mutation) {
                                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                                    setAdTheme();
                                }
                            });
                        };
                        
                        const observer = new MutationObserver(callback);
                        observer.observe(document.documentElement, { attributes: true });

                        window.onresize = () => {
                            if (window.innerWidth >= 1280 && ad_container_main.childElementCount == 0) {
                                ad_container_main.appendChild(ad_element);
                                ad_element.removeAttribute("data-ea-type");
                                ad_element.querySelectorAll("img")[0].style.display = "block";
                                ad_element.querySelectorAll(".ea-placement")[0].classList.add("ea-type-image")
                                ad_element.querySelectorAll(".ea-placement")[0].classList.remove("ea-type-text")
                            } else if (window.innerWidth < 1280 && ad_container_alt.childElementCount == 0) {
                                ad_container_alt.appendChild(ad_element);
                                ad_element.setAttribute("data-ea-type", "text");
                                ad_element.querySelectorAll("img")[0].style.display = "none";
                                ad_element.querySelectorAll(".ea-placement")[0].classList.add("ea-type-text")
                                ad_element.querySelectorAll(".ea-placement")[0].classList.remove("ea-type-image")
                            }
                        };

                        window.onload = () => {
                            setAdTheme();
                            window.onresize();
                        };
                        window.onready = () => {
                            setAdTheme();
                            window.onresize();
                        };
                        setTimeout(window.onresize, 1000);
                    `}</Script>
                </>
            )
        }
    },
    main: (children) => {
        return (
            <>
                {children.children}
                <div id="ad-docs-toc-alt"></div>
            </>
        )
    },
    defaultShowCopyCode: true,
    nextThemes: {
        defaultTheme: 'dark'
    }
}
