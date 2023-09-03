import React from "react"
import { useRouter } from "next/router"
import { useConfig } from "nextra-theme-docs"
import { UserCircleIcon } from "@heroicons/react/24/outline"
import useSWR from "swr"
import CatIcon from "./src/components/icons/Cat";

import Link from "next/link"
import Script from "next/script"

import Popup from "./src/components/popup"
import contributors from "./src/constants/contributors"

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

const UserButton = () => {
    const { user, error, isLoading } = useUser()

    if (isLoading) return <div className="m-0.5 h-6 w-6 rounded-full border-2 border-[hsl(var(--nextra-primary-hue),100%,50%)] border-t-transparent animate-spin"></div>
    if (error || (user && "errors" in user)) {
        return (
            <Popup
                trigger={(
                    <UserCircleIcon className="h-7 w-7" />
                )}
                triggerContainerClassName="flex flex-col items-center justify-center w-7 h-7 cursor-pointer"
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

    return <img src={user.data.attributes.avatarImage} className="rounded-full object-cover h-7 w-7 min-w-7" />
}


export default {
    logo: () => {
        return (
            <div style={{ display: "flex", flexDirection: "row", alignItems: "center", gap: "1rem" }}>
                <img src="/branding/logo/logo.png" alt="Logo" width={32} height={32} />
                <span>Nekos API</span>
                <div className="hidden md:block font-mono p-1 rounded border dark:border-neutral-700 dark:bg-neutral-800 border-neutral-200 bg-neutral-100 text-sm leading-none h-fit">{process.env.NEXT_PUBLIC_NEKOS_API_VERSION}</div>
            </div>
        )
    },
    project: {
        link: 'https://github.com/Nekos-API/Nekos-API',
    },
    docsRepositoryBase: "https://github.com/Nekos-API/Nekos-API/tree/main/docs",
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
            <meta property="og:title" content={frontMatter.title || 'Nekos API - Unleash the Meow-nificent Power of +17.5k Anime Images, GIFs, and More!'} />
            <meta property="og:description" content={frontMatter.description || 'Discover +13.5k high-quality anime images & GIFs for UwU-filled adventures. Explore artists, categories, and adorable characters. Embark on purrfect anime journeys now!'} />
            <meta property="og:image" content="/imgs/banners/banner.jfif" />

            <meta name="description" content={frontMatter.description || "Discover +13.5k high-quality anime images & GIFs for UwU-filled adventures. Explore artists, categories, and adorable characters. Embark on purrfect anime journeys now!"} />
            <meta name="theme-color" content="#ff0055" />

            <meta property="twitter:card" content="summary_large_image" />
            <meta property="twitter:url" content="https://nekosapi.com/" />
            <meta property="twitter:title" content="Nekos API - Unleash the Meow-nificent Power of +17.5k Anime Images, GIFs, and More!" />
            <meta property="twitter:description" content="Discover +13.5k high-quality anime images & GIFs for UwU-filled adventures. Explore artists, categories, and adorable characters. Embark on purrfect anime journeys now!" />
            <meta property="twitter:image" content="/imgs/banners/banner.jfif" />
        </>
    },
    primaryHue: {
        light: 350,
        dark: 340,
    },
    chat: {
        "link": "https://discord.gg/PgQnuM3YnM"
    },
    banner: {
        "key": "join-our-discord-server",
        "text": (
            <Link href="https://nekosauce.org" style={{ display: "flex", flexDirection: "row", alignItems: "center", justifyContent: "center", gap: ".5rem" }}>
                ✨ We're launching NekoSauce, an anime and manga sauce finder! If you like this project, please consider making a donation ✨
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" style={{ height: "1rem", width: "1rem" }}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                </svg>
            </Link>
        ),
        "dismissible": false
    },
    footer: {
        text: () => {
            const [status, setStatus] = React.useState();
            const [error, setError] = React.useState();
            const [isLoading, setIsLoading] = React.useState(true);

            React.useEffect(() => {
                fetch('/api/status', { cache: "no-store" }).then(res => res.json()).then((data) => {
                    setStatus(data.status)
                }).catch((e) => {
                    setError(e)
                }).finally(() => {
                    setIsLoading(false)
                })
            }, [])

            return (
                <div className="flex flex-col md:flex-row md:items-center justify-between w-full gap-4">
                    <div>
                        MIT {new Date().getFullYear()} © <a href="https://nekidev.com" target="_blank" className="hover:underline">Nekidev</a>. Made with
                        <div className="h-4 inline-block overflow-hidden group relative leading-none -mb-0.5 mx-1 cursor-default">
                            <div className="group-hover:-mt-4 transition-all">❤</div>
                            <CatIcon className="h-4 w-4" />
                        </div>
                        from Argentina, <Link className="hover:underline" href="https://google.com/search?q=argentina+vs+france+2022+world+cup+results" target="_blank">the football world champion 🏆 ⭐⭐⭐</Link>.
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
                        ) : error || (status != undefined && status != "up") ? (
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
            return <div className="flex flex-row items-center gap-5 ml-1.5">
                {/* <Link href="https://nekos.land" target="_blank">
                    <svg width="648" height="648" viewBox="0 0 648 648" fill="currentColor" xmlns="http://www.w3.org/2000/svg" className="h-7 w-7">
                        <g>
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M62.3705 107.926C60.1685 99.1344 68.1344 91.1685 76.9264 93.3705L230.892 131.933C233.354 132.55 235.945 132.361 238.313 131.449C265.065 121.151 294.127 115.507 324.507 115.507C354.745 115.507 383.677 121.099 410.325 131.305C412.688 132.21 415.271 132.396 417.726 131.781L571.087 93.3705C579.879 91.1685 587.845 99.1344 585.643 107.926L547.472 260.329C546.848 262.818 547.048 265.438 547.986 267.827C558.651 294.987 564.507 324.563 564.507 355.507C564.507 488.055 457.055 555.507 324.507 555.507C191.958 555.507 84.5066 488.055 84.5066 355.507C84.5066 325.127 90.1513 296.065 100.449 269.313C101.361 266.945 101.55 264.354 100.933 261.892L62.3705 107.926ZM124.128 159.98C123.394 157.049 126.049 154.394 128.98 155.128L190.943 170.647C193.958 171.402 194.998 175.158 192.8 177.356L146.356 223.8C144.158 225.998 140.402 224.958 139.647 221.943L124.128 159.98ZM520.033 155.128C522.964 154.394 525.619 157.049 524.885 159.98L509.366 221.943C508.611 224.958 504.855 225.998 502.657 223.8L456.214 177.356C454.016 175.158 455.055 171.402 458.07 170.647L520.033 155.128Z" />
                        </g>
                    </svg>
                </Link> */}
                <UserButton />
            </div>
        }
    },
    search: {
        emptyResult: () => {
            return (
                <div className="flex flex-col gap-2 items-center justify-center h-[100px] text-neutral-500 text-sm">
                    <svg width="648" height="648" viewBox="0 0 648 648" fill="currentColor" xmlns="http://www.w3.org/2000/svg" className="h-6 w-6">
                        <g>
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M62.3705 107.926C60.1685 99.1344 68.1344 91.1685 76.9264 93.3705L230.892 131.933C233.354 132.55 235.945 132.361 238.313 131.449C265.065 121.151 294.127 115.507 324.507 115.507C354.745 115.507 383.677 121.099 410.325 131.305C412.688 132.21 415.271 132.396 417.726 131.781L571.087 93.3705C579.879 91.1685 587.845 99.1344 585.643 107.926L547.472 260.329C546.848 262.818 547.048 265.438 547.986 267.827C558.651 294.987 564.507 324.563 564.507 355.507C564.507 488.055 457.055 555.507 324.507 555.507C191.958 555.507 84.5066 488.055 84.5066 355.507C84.5066 325.127 90.1513 296.065 100.449 269.313C101.361 266.945 101.55 264.354 100.933 261.892L62.3705 107.926ZM124.128 159.98C123.394 157.049 126.049 154.394 128.98 155.128L190.943 170.647C193.958 171.402 194.998 175.158 192.8 177.356L146.356 223.8C144.158 225.998 140.402 224.958 139.647 221.943L124.128 159.98ZM520.033 155.128C522.964 154.394 525.619 157.049 524.885 159.98L509.366 221.943C508.611 224.958 504.855 225.998 502.657 223.8L456.214 177.356C454.016 175.158 455.055 171.402 458.07 170.647L520.033 155.128Z" />
                        </g>
                    </svg>
                    No cats found.
                </div>
            )
        }
    },
    sidebar: {
        defaultMenuCollapseLevel: 1,
        toggleButton: true,
    },
    toc: {
        backToTop: false,
        title: "On This UwU Page"
        // extraContent: () => {
        //     return (
        //         <>
        //             <Script async={true} src="https://media.ethicalads.io/media/client/ethicalads.min.js" />
        //             <div id="ad-docs-toc-main">
        //                 <div className="bordered" data-ea-publisher="nekosapicom" id="ad-docs-toc"></div>
        //             </div>
        //             <Script>{`
        //                 const ad_container_main = document.getElementById("ad-docs-toc-main");
        //                 const ad_container_alt = document.getElementById("ad-docs-toc-alt");
        //                 const ad_element = document.getElementById("ad-docs-toc");

        //                 function setAdTheme() {
        //                     if (document.documentElement.className.includes("dark")) {
        //                         ad_element.classList.add("dark");
        //                     } else {
        //                         ad_element.classList.remove("dark");
        //                     }
        //                 };

        //                 function callback(mutationList, observer) {
        //                     mutationList.forEach(function(mutation) {
        //                         if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
        //                             setAdTheme();
        //                         }
        //                     });
        //                 };

        //                 const observer = new MutationObserver(callback);
        //                 observer.observe(document.documentElement, { attributes: true });

        //                 window.onresize = () => {
        //                     if (window.innerWidth >= 1280 && ad_container_main.childElementCount == 0) {
        //                         ad_container_main.appendChild(ad_element);
        //                         ad_element.removeAttribute("data-ea-type");
        //                         ad_element.querySelectorAll("img")[0].style.display = "block";
        //                         ad_element.querySelectorAll(".ea-placement")[0].classList.add("ea-type-image")
        //                         ad_element.querySelectorAll(".ea-placement")[0].classList.remove("ea-type-text")
        //                     } else if (window.innerWidth < 1280 && ad_container_alt.childElementCount == 0) {
        //                         ad_container_alt.appendChild(ad_element);
        //                         ad_element.setAttribute("data-ea-type", "text");
        //                         ad_element.querySelectorAll("img")[0].style.display = "none";
        //                         ad_element.querySelectorAll(".ea-placement")[0].classList.add("ea-type-text")
        //                         ad_element.querySelectorAll(".ea-placement")[0].classList.remove("ea-type-image")
        //                     }
        //                 };

        //                 window.onload = () => {
        //                     setAdTheme();
        //                     window.onresize();
        //                 };
        //                 window.onready = () => {
        //                     setAdTheme();
        //                     window.onresize();
        //                 };
        //                 setTimeout(window.onresize, 1000);
        //             `}</Script>
        //         </>
        //     )
        // }
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
    },
    components: {
        "a": ({ children, href, ...props }) => {
            return <Link className="text-[hsl(var(--nextra-primary-hue)100%_45%/var(--tw-text-opacity))] text-primary-600 no-underline hover:underline decoration-from-font [text-underline-position:from-font]" href={href} {...props}>{children}</Link>
        }
    },
    gitTimestamp: () => {
        const router = useRouter();

        const [commitData, setCommitData] = React.useState();
        const [isLoading, setIsLoading] = React.useState(true);
        const [error, setError] = React.useState();

        React.useEffect(() => {
            setError(false)
            setIsLoading(true)
            fetch(
                `https://api.github.com/repos/Nekos-API/Nekos-API/commits?path=/docs/src/pages${['/', '/docs'].includes(router.pathname) ?
                    router.pathname + '/index.mdx' :
                    router.pathname + ".mdx"
                }`)
                .then((data) => data.json())
                .then((data) => {
                    setCommitData(data)
                    setIsLoading(false)
                    setError(false)
                })
                .catch((e) => {
                    setCommitData(null)
                    setError(true)
                    setIsLoading(false)
                })
        }, [router.asPath])

        const Contributor = ({ username, image, url }) => {
            return (
                <Link href={url} className="relative flex flex-col items-center" target="_blank">
                    <img src={image} className="h-7 w-7 object-cover block hover:scale-110 transition-all rounded-full peer" />
                    <div className="absolute bottom-full bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 drop-shadow-md rounded mx-auto whitespace-nowrap flex flex-col items-center py-1 px-2 transition-all opacity-0 mb-0 peer-hover:opacity-100 peer-hover:mb-2 text-neutral-900 dark:text-[#f1f5f9] pointer-events-none after:absolute after:-bottom-1 after:left-0 after:right-0 after:mx-auto after:w-2 after:h-2 after:rotate-45 after:rounded-sm after:bg-white after:dark:bg-neutral-900 after:border after:border-neutral-200 after:dark:border-neutral-800 after:!border-t-transparent after:!border-l-transparent">
                        <span className="text-xs">{username}</span>
                    </div>
                </Link>
            )
        }

        var commitAuthors = []
        var commiterAuthorIDs = []

        var commitDates = []

        if (commitData) {
            for (const commit of commitData) {
                const authorData = {
                    username: commit.author.login,
                    image: commit.author.avatar_url,
                    url: commit.author.html_url
                }

                if (!commiterAuthorIDs.includes(commit.author.login)) {
                    commitAuthors.push(authorData)
                    commiterAuthorIDs.push(commit.author.login)
                }
            }

            commitDates = commitData.map((value, index) => value.commit.committer.date).sort(function (a, b) {
                return Date.parse(a) > Date.parse(b);
            });
        }

        return (
            <div className="w-full text-left block">
                <div className="flex flex-row gap-2 mb-3">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 mt-1">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
                    </svg>
                    <div className="flex flex-row gap-4 flex-wrap">
                        {(!isLoading && !error) ? commitAuthors.map((value, index) => {
                            return <Contributor {...value} key={index} />
                        }) : (
                            <>...</>
                        )}
                    </div>
                </div>
                <div className="w-full text-left inline-flex flex-col md:flex-row gap-3 md:gap-4 md:items-center">
                    <div className="flex flex-row items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Created on {(!isLoading && !error) ? (
                            new Date(commitDates[commitDates.length - 1])
                        ).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) : (
                            <>...</>
                        )}
                    </div>
                    <div className="flex flex-row items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
                        </svg>
                        Last updated on {(!isLoading && !error) ? (new Date(commitDates[0])).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) : (
                            <>...</>
                        )}
                    </div>
                </div>
            </div>
        )
    }
}
