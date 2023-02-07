"use client"

import React from "react";

import Link from "next/link";

import { ArrowLeftOnRectangleIcon, ArrowUpTrayIcon, Cog6ToothIcon, ExclamationCircleIcon, MagnifyingGlassIcon, RectangleStackIcon, UserIcon } from "@heroicons/react/24/outline";
import { ScalePrimaryButton, ScaleBorderButton } from "../button";

import Auth from "@/utils/authorization";

import Popup from "@/components/popup";

export default function Navbar() {
    const auth = new Auth();
    const { user, error, isLoading } = auth.useUser();

    return (
        <div className="sticky top-0 left-0 right-0 bg-white flex flex-col items-center justify-center leading-none p-4 z-50 border-b-2 border-b-neutral-100">
            <div className="w-full max-w-5xl flex flex-row items-center justify-between text-neutral-800 font-extrabold text-lg">
                <div className="flex flex-row items-center gap-8">
                    <NavbarLink href="/">Home</NavbarLink>
                    <NavbarLink href="/search">Search</NavbarLink>
                    <NavbarLink href="/explore">Explore</NavbarLink>
                    <NavbarLink href="/library">Library</NavbarLink>
                </div>
                <div className="flex flex-row items-center gap-4">
                    <Link href="/search">
                        <MagnifyingGlassIcon className="h-5 w-5 stroke-[2.5] transition hover:text-crayola-300 cursor-pointer" />
                    </Link>
                    {(user || isLoading) && (
                        <Link href="/uploads/create">
                            <ArrowUpTrayIcon className="h-5 w-5 stroke-[2.5] transition hover:text-crayola-300 cursor-pointer" />
                        </Link>
                    )}
                    <div className="w-0.5 rounded-full h-6 bg-neutral-200"></div>
                    {isLoading ? (
                        <div className="h-5 w-5 border-2 border-crayola-350 border-t-transparent rounded-full animate-spin"></div>
                    ) : error ? (
                        <ExclamationCircleIcon className="h-5 w-5 stroke-crayola-350" />
                    ) : user ? (
                        <Popup
                            trigger={(
                                <div className="flex flex-row items-center gap-4 cursor-pointer -my-2 group relative">
                                    <div className="font-bold text-base relative group-hover:text-crayola-350 transition-colors">{user.attributes.username}</div>
                                    <img src={user.attributes.avatarImage} className="h-8 w-8 rounded-full object-cover hover:drop-shadow-sm cursor-pointer bg-white relative border-2 border-neutral-200" />
                                </div>
                            )}
                            on="click"
                            alignment="bottom-right"
                            popupContainerClassName="pt-6"
                            initialAnim={{
                                y: -8,
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
                                y: -8,
                                opacity: 0,
                                transition: {
                                    duration: .1
                                }
                            }}>
                            <div className="bg-white rounded-b-md border-2 border-t-0 border-neutral-100 font-medium text-base py-2 relative flex flex-col w-48">
                                <Link href="/profile" className="px-4 py-2 leading-none hover:bg-neutral-100 transition w-full flex flex-row items-center gap-2" >
                                    <UserIcon className="h-5 w-5" />
                                    Profile
                                </Link>
                                <Link href="/settings" className="px-4 py-2 leading-none hover:bg-neutral-100 transition w-full flex flex-row items-center gap-2" >
                                    <Cog6ToothIcon className="h-5 w-5" />
                                    Settings
                                </Link>
                                <Link href="/uploads" className="px-4 py-2 leading-none hover:bg-neutral-100 transition w-full flex flex-row items-center gap-2" >
                                    <ArrowUpTrayIcon className="h-5 w-5" />
                                    Uploads
                                </Link>
                                <Link href="/library" className="px-4 py-2 leading-none hover:bg-neutral-100 transition w-full flex flex-row items-center gap-2" >
                                    <RectangleStackIcon className="h-5 w-5" />
                                    Library
                                </Link>
                                <div className="w-full h-0.5 bg-neutral-100 my-2"></div>
                                <div className="px-4 py-2 leading-none hover:bg-neutral-100 transition w-full flex flex-row items-center gap-2 cursor-pointer" onClick={() => {
                                    auth.logout();
                                }} >
                                    <ArrowLeftOnRectangleIcon className="h-5 w-5" />
                                    Log out
                                </div>
                            </div>
                        </Popup>
                    ) : (
                        <div className="-my-3 flex flex-row items-center gap-4">
                            <Link href="/login">
                                <ScalePrimaryButton>Log in</ScalePrimaryButton>
                            </Link>
                            <Link href="/signup">
                                <ScaleBorderButton>Sign up</ScaleBorderButton>
                            </Link>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

function NavbarLink({ href, children }) {
    return (
        <Link className="transition relative group/link" href={href}>
            {/* <div className="absolute -top-2 -bottom-2 -left-4 -right-4 bg-crayola-50 rounded-full scale-50 opacity-0 transition-all group-hover/link:scale-100 group-hover/link:opacity-100"></div> */}
            <div className="z-10 relative group-hover/link:text-crayola-350 transition-colors">
                {children}
            </div>
        </Link>
    )
}