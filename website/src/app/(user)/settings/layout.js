"use client";

import Auth from "@/utils/authorization";
import {
    ArrowsRightLeftIcon,
    BoltIcon,
    CheckBadgeIcon,
    ClockIcon,
    CodeBracketIcon,
    Cog6ToothIcon,
    DocumentTextIcon,
    HeartIcon,
    QuestionMarkCircleIcon,
    ScaleIcon,
    UserIcon,
    WindowIcon,
} from "@heroicons/react/24/outline";
import Link from "next/link";
import { usePathname } from "next/navigation";
import React from "react";

export default function Layout({ children }) {
    const auth = new Auth();

    const { user, error, isLoading } = auth.useUser();

    return (
        <div className="flex flex-col gap-8 w-full relative py-4">
            <div className="flex flex-row gap-4 items-center">
                {isLoading ? (
                    <>
                        <div className="h-12 w-12 bg-neutral-200 animate-pulse rounded-full"></div>
                        <div>
                            <div className="text-xl font-extrabold leading-none text-transparent rounded bg-neutral-200 animate-pulse mb-1">
                                AAAAAAAA
                            </div>
                            <div className="text-neutral-500 text-base leading-none text-transparent rounded bg-neutral-200 animate-pulse">
                                aaaaaaaaaaaaa
                            </div>
                        </div>
                    </>
                ) : error ? (
                    <>Error</>
                ) : (
                    <>
                        <img
                            src={user.attributes.avatarImage}
                            className="h-12 w-12 object-cover rounded-full"
                        />
                        <div>
                            <div className="text-xl font-extrabold leading-none mb-1">
                                {user.attributes.username}
                            </div>
                            <div className="text-neutral-500 text-base leading-none">
                                {user.attributes.email}
                            </div>
                        </div>
                    </>
                )}
            </div>
            <div className="grid grid-cols-[2fr_7fr] relative w-full gap-6">
                <div className="w-full border-r-2 border-neutral-100 pr-6 flex flex-col gap-1">
                    <PageLinkDivider>Me</PageLinkDivider>
                    <PageLink
                        title="Profile"
                        icon={<UserIcon />}
                        href="/settings/profile"
                    />
                    <PageLink
                        title="Account"
                        icon={<Cog6ToothIcon />}
                        href="/settings/account"
                    />
                    <PageLink
                        title="Connections"
                        icon={<ArrowsRightLeftIcon />}
                        href="/settings/connections"
                    />

                    <PageLinkDivider>Uploads</PageLinkDivider>
                    <PageLink
                        title="Verified uploads"
                        icon={<CheckBadgeIcon />}
                        href="/settings/verified-uploads"
                    />
                    <PageLink
                        title="Pending verification"
                        icon={<ClockIcon />}
                        href="/settings/uploads-pending-verification"
                    />

                    <PageLinkDivider>Developers</PageLinkDivider>
                    <PageLink
                        title="Aplications"
                        icon={<CodeBracketIcon />}
                        href="/settings/applications"
                    />
                    <PageLink
                        title="Webhooks"
                        icon={<BoltIcon />}
                        href="/settings/webhooks"
                    />
                    <PageLink
                        title="Embeds"
                        icon={<WindowIcon />}
                        href="/settings/embeds"
                    />
                    <PageLink
                        title="Documentation"
                        icon={<DocumentTextIcon />}
                        href="https://docs.nekosapi.com"
                    />

                    <PageLinkDivider>Legal</PageLinkDivider>
                    <PageLink
                        title="Terms of use"
                        icon={<ScaleIcon />}
                        href="/terms-of-use"
                    />
                    <PageLink
                        title="Privacy policy"
                        icon={<ScaleIcon />}
                        href="/privacy-policy"
                    />
                    <PageLink
                        title="Disclaimer"
                        icon={<ScaleIcon />}
                        href="/disclaimer"
                    />

                    <PageLinkDivider>More</PageLinkDivider>
                    <PageLink
                        title="About"
                        icon={<QuestionMarkCircleIcon />}
                        href="/about"
                    />
                    <PageLink
                        title="Donate"
                        icon={<HeartIcon />}
                        href="/donate"
                    />
                </div>
                <div>{children}</div>
            </div>
        </div>
    );
}

function PageLink({ title, icon, href }) {
    const pathname = usePathname();

    return (
        <Link
            href={href}
            className={
                "flex flex-row items-center gap-2 py-2 group relative transition" +
                (pathname.startsWith(href) ? " text-crayola-350" : "")
            }
        >
            <div
                className={
                    "absolute top-0 bottom-0 -left-3 -right-3 rounded-full -z-10 transition-all " +
                    (pathname.startsWith(href)
                        ? "bg-crayola-50 group-hover:scale-105"
                        : "scale-75 opacity-0 group-hover:scale-100 group-hover:opacity-100 bg-neutral-100")
                }
            ></div>
            <div className="h-5 w-5">{icon}</div>
            <span>{title}</span>
        </Link>
    );
}

function PageLinkDivider({ children }) {
    return (
        <div className="text-xs uppercase mb-2 mt-6 first:mt-0 text-neutral-400 flex flex-row items-center gap-2">
            <div className="h-1 rounded-full w-5 bg-neutral-100"></div>
            {children}
        </div>
    );
}
