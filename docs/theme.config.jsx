import React from "react"
import { useRouter } from "next/router"
import { useConfig } from "nextra-theme-docs"
import { UserCircleIcon, ChevronDownIcon } from "@heroicons/react/24/outline"
import useSWR from "swr"
import CatIcon from "./src/components/icons/Cat";
import Link from "next/link"

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


function VersionOption({ label, stable = false, href }) {
    return (
        <Link href={href} className="rounded hover:bg-neutral-800 transition flex flex-row items-center gap-1 pr-1 leading-none text-sm font-mono">
            {stable ? (
                <div className="bg-blue-400/20 text-blue-400 rounded aspect-square h-4 w-4 text-center">
                    S
                </div>
            ) : (
                <div className="bg-yellow-400/20 text-yellow-400 rounded aspect-square h-4 w-4 text-center">
                    D
                </div>
            )}
            <span>{label}</span>
        </Link>
    )
}


export default {
    logo: () => {
        return (
            <div className="flex items-center gap-4">
                <Link className="flex flex-row items-center gap-4 hover:opacity-75" href="/">
                    <img src="/branding/logo/logo.png" alt="Logo" width={32} height={32} />
                    <span>Nekos API</span>
                </Link>
                <Popup
                    trigger={(
                        <button className="hidden md:flex flex-row items-center rounded transition hover:bg-neutral-900 border border-neutral-700">
                            <div className="flex flex-row items-center gap-1 font-mono p-1 rounded border dark:border-neutral-700 dark:bg-neutral-800 border-neutral-200 bg-neutral-100 text-sm leading-none h-fit -my-px -ml-px">
                                {process.env.NEXT_PUBLIC_NEKOS_API_VERSION}
                            </div>
                            <ChevronDownIcon className="h-6 w-6 p-1.5 -my-px" />
                        </button>
                    )}
                    alignment="bottom-left"
                    popupContainerClassName="pt-2"
                    initialAnim={{
                        y: -5,
                        opacity: 0,
                        transition: {
                            duration: .1
                        }
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
                    <div className="bg-neutral-900 border border-neutral-800 rounded p-1 flex flex-col gap-1">
                        <VersionOption label={process.env.NEXT_PUBLIC_NEKOS_API_VERSION} href="" stable />
                        <VersionOption label="v1.6.0" href="https://v1.nekosapi.com" />
                        <VersionOption label="v0.3.0" href="https://v0.nekosapi.com" />
                    </div>
                </Popup>
            </div>
        )
    },
    logoLink: false,
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
            <Link href="/donate" style={{ display: "flex", flexDirection: "row", alignItems: "center", justifyContent: "center", gap: ".5rem", whiteSpace: "pre-wrap" }}>
                ✨ Nekos API is slowly running out of resources. If you enjoy this project, please consider making a donation. Click here to learn more. ✨
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
                <Link
                    href={`https://ko-fi.com/nekidev`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="m-2 h-6 w-6"
                >
                    <svg
                        width="24"
                        height="24"
                        className="scale-125"
                        viewBox="0 0 124 81"
                        fill="currentColor"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M0 8C0 3.58173 3.58154 0 8 0H90V0.0977478C90.8247 0.0329895 91.6587 0 92.5 0C109.897 0 124 14.103 124 31.5C124 48.897 109.897 63 92.5 63C92.024 63 91.5504 62.9894 91.0794 62.9685C90.4969 62.9427 90 63.4007 90 63.9838V65C90 73.8365 82.8364 81 74 81H16C7.16357 81 0 73.8365 0 65V8ZM6 8C6 6.89542 6.89551 6 8 6H48H85H92C106.359 6 118 17.6406 118 32C118 46.3594 106.359 58 92 58H87C85.8954 58 85 58.8954 85 60V64C85 70.6274 79.6274 76 73 76H16C10.4771 76 6 71.5229 6 66V8Z"
                        />
                        <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M88 15C86.3431 15 85 16.3431 85 18V45C85 46.6569 86.3431 48 88 48H92.5C101.613 48 109 40.6127 109 31.5C109 22.3873 101.613 15 92.5 15H88ZM90.7778 20C90.3482 20 90 20.3482 90 20.7778V42.2222C90 42.6518 90.3482 43 90.7778 43H92.5C98.8513 43 104 37.8513 104 31.5C104 25.1487 98.8513 20 92.5 20H90.7778Z"
                        />
                        <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M24.8489 23.3721C19.6728 28.5482 19.6728 36.9403 24.8489 42.1164L45.5774 62.8449L45.6609 62.7615L45.7444 62.8449L66.4729 42.1164C71.649 36.9403 71.649 28.5482 66.4729 23.3721C61.2968 18.196 52.9047 18.196 47.7286 23.3721L45.6609 25.4398L43.5932 23.3721C38.4171 18.196 30.025 18.196 24.8489 23.3721Z"
                        />
                    </svg>
                </Link>
                {/* <UserButton /> */}
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
        backToTop: true,
        title: "On This UwU Page"
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
    },
    editLink: {
        text: "Edit this page on GitHub →"
    }
}
