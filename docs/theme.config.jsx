import { useRouter } from "next/router"
import { useConfig } from "nextra-theme-docs"

import Link from "next/link"
import Script from "next/script"

export default {
    logo: () => {
        const { asPath } = useRouter()
        return (
            <div style={{ display: "flex", flexDirection: "row", alignItems: "center", gap: "1rem" }}>
                <img src="/logo/black.png" alt="Logo" width={32} height={32} />
                <span>Nekos API {asPath.startsWith('/docs') && "Documentation"}</span>
            </div>
        )
    },
    project: {
        link: 'https://github.com/Nekidev/Nekos-API',
    },
    docsRepositoryBase: "https://github.com/Nekidev/Nekos-API",
    useNextSeoProps() {
        const { route } = useRouter()
        if (route !== '/') {
            return {
                titleTemplate: '%s – Nekos API'
            }
        } else {
            return {
                titleTemplate: 'Nekos API'
            }
        }
    },
    head: () => {
        const { asPath } = useRouter()
        const { frontMatter } = useConfig()
        return <>
            <meta property="og:url" content={`https://nekosapi.com${asPath}`} />
            <meta property="og:title" content={frontMatter.title || 'Nekos API Documentation'} />
            <meta property="og:description" content={frontMatter.description || 'The open-source free public anime images Restful/GraphQL API.'} />
            <meta name="description" content={frontMatter.description || 'The open-source free public anime images Restful/GraphQL API.'} />
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
        "key": "v2-almost-finished",
        "text": (
            <Link href="https://github.com/Nekos-API/Nekos-API" style={{ display: "flex", flexDirection: "row", alignItems: "center", justifyContent: "center", gap: ".5rem" }}>
                ✨ <span className="font-mono">v2.0.0-alpha</span> is almost finished! You can check out the current progress at it's GitHub repository ✨
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" style={{ height: "1rem", width: "1rem" }}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                </svg>
            </Link>
        )
    },
    footer: {
        "text": (
            <span>
                MIT {new Date().getFullYear()} © <a href="https://nekidev.com" target="_blank">Nekidev</a>. Made with ❤ from Argentina.
            </span>
        )
    },
    sidebar: {
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
                                console.log("appended to main")
                            } else if (window.innerWidth < 1280 && ad_container_alt.childElementCount == 0) {
                                ad_container_alt.appendChild(ad_element);
                                ad_element.setAttribute("data-ea-type", "text");
                                ad_element.querySelectorAll("img")[0].style.display = "none";
                                ad_element.querySelectorAll(".ea-placement")[0].classList.add("ea-type-text")
                                ad_element.querySelectorAll(".ea-placement")[0].classList.remove("ea-type-image")
                                console.log("appended to alt")
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
            <div>
                {children.children}
                <div id="ad-docs-toc-alt"></div>
            </div>
        )
    },
    defaultShowCopyCode: true,
}
