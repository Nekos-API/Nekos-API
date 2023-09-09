import 'nextra-theme-docs/style.css'
import '../styles/nprogress.css'
import '../styles/globals.css'

import Router from "next/router";
import NProgress from "nprogress"
import { Analytics } from '@vercel/analytics/react';

import { Rubik } from 'next/font/google';
import Link from 'next/link';

import contributors from '../constants/contributors';

Router.events.on("routeChangeStart", () => NProgress.start());
Router.events.on("routeChangeComplete", () => NProgress.done());
Router.events.on("routeChangeError", () => NProgress.done());

NProgress.configure({ showSpinner: false });

const asap = Rubik({ subsets: ["latin"] });

const Contributor = ({ username, image, url }) => {
    return (
        <Link href={url} className="relative flex flex-col items-center" target="_blank">
            <img src={image} loading="lazy" className="h-7 w-7 object-cover block hover:scale-110 transition-all rounded-full peer" />
            <div className="absolute bottom-full bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 drop-shadow-md rounded mx-auto whitespace-nowrap flex flex-col items-center py-1 px-2 transition-all opacity-0 mb-0 peer-hover:opacity-100 peer-hover:mb-2 text-neutral-900 dark:text-[#f1f5f9] pointer-events-none after:absolute after:-bottom-1 after:left-0 after:right-0 after:mx-auto after:w-2 after:h-2 after:rotate-45 after:rounded-sm after:bg-white after:dark:bg-neutral-900 after:border after:border-neutral-200 after:dark:border-neutral-800 after:!border-t-transparent after:!border-l-transparent">
                <span className="text-xs">{username}</span>
            </div>
        </Link>
    )
}

export default function NekosAPI({ Component, pageProps }) {
    return (
        <div className={asap.className + " "}>
            <Component {...pageProps} />
            <hr className="dark:border-neutral-800" />
            <div
                className={
                    'mx-auto flex flex-col-reverse lg:flex-row w-full max-w-[90rem] lg:items-center justify-between py-2 text-gray-600 dark:text-gray-400 pl-[max(env(safe-area-inset-left),1.5rem)] pr-[max(env(safe-area-inset-right),1.5rem)] bg-gray-100 dark:bg-neutral-900 print:bg-transparent text-sm gap-8'
                }
            >
                <div className='flex flex-row items-center justify-between gap-x-8 gap-y-2 flex-wrap'>
                    <Link href="https://nyeki.dev/">Nyeki.py</Link>
                    <Link href="https://nekos.land/">Nekos.Land</Link>
                    <Link href="https://nekosauce.org/">NekoSauce</Link>
                    <Link href="https://github.com/Nekos-API/Nekos-API">GitHub</Link>
                    <Link href="https://status.nekosapi.com/">Status</Link>
                    <Link href="https://discord.gg/PgQnuM3YnM">Discord</Link>
                    <Link href="/donate">Donate</Link>
                </div>
                <div className='flex flex-row items-center gap-2 justify-between sm:justify-start'>
                    <span className="hidden sm:inline-block">Thanks to:</span>
                    {contributors.map((contributor) => (
                        <Contributor
                            key={contributor.id}
                            username={contributor.name}
                            image={`https://nekosapi.com/api/discord/avatar?user_id=${contributor.id}`}
                            url={`https://discord.com/users/${contributor.id}`}
                        />
                    ))}
                </div>
            </div>
            <Analytics />
        </div>
    )
}