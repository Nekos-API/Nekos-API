"use client";

import React from "react";
import { LightPrimaryButton, ScaleBorderButton } from "@/components/button";
import {
    ArrowRightIcon,
    ExclamationCircleIcon,
    HashtagIcon,
    HeartIcon,
} from "@heroicons/react/24/outline";
import Link from "next/link";
import useSWR from "swr";
import colcade from "colcade";
import styles from "./page.module.css";

const fetcher = (url) =>
    fetch(process.env.NEXT_PUBLIC_API_BASE + url, {
        headers: {
            Accept: "application/vnd.api+json",
        },
    }).then((res) => res.json());

export default function Home() {
    const [betaMessage, setBetaMessage] = React.useState(false);

    React.useEffect(() => {
        if (!localStorage.getItem("betaMessage")) {
            setBetaMessage(true);
        }
    }, [])

    return (
        <div className="py-8 grid grid-cols-[5fr_2fr] gap-12 max-w-5xl relative">
            <div className="max-w-full">
                <h2 className="text-3xl font-extrabold text-neutral-800">
                    Welcome to Nekos Web!
                </h2>
                <p className="mt-2 mb-12 text-neutral-500">
                    Nekos Web is one of the biggest collections of anime images.
                    You can look at what other people upload, or upload images
                    yourself!
                </p>
                {betaMessage && (
                    <div className="bg-crayola-350 flex flex-row p-4 gap-4 text-white rounded-lg w-full -mt-4 mb-8">
                        <ExclamationCircleIcon className="h-6 w-6" />
                        <div className="flex flex-col gap-2 flex-1">
                            <div className="font-bold text-xl">Beta version ahead!</div>
                            <p>
                                Hello, and welcome to the Nekos Web beta version! As it name says, this is a beta version. This means that most things will not be working properly or completely missing. This website was created to allow developers to create applications to make use of Nekos API and will probably stay like that while we finish the beta version of Nekos API.
                                <br /> <br />
                                We are always open to contributions and if you cannot wait to see this project finished you can always make your PR to our <Link href="https://github.com/Nekos-API/Nekos-API" className="underline hover:decoration-transparent">GitHub repository</Link>.
                                <br /> <br />
                                This does not mean that the project is abandoned or that it will not be continued. We will continue with this website as soon as a stable version of Nekos API is released.
                            </p>
                            <div className="flex flex-row items-center mt-2 gap-2">
                                <button className="text-crayola-350 bg-white py-3 px-4 rounded-lg leading-none w-fit" onClick={() => {
                                    localStorage.setItem("betaMessage", "shown");
                                    setBetaMessage(false);
                                }}>I understand, now close this</button>
                                <Link href="https://github.com/Nekos-API/Nekos-API">
                                    <button className="text-white bg-crayola-300 py-3 px-4 rounded-lg leading-none w-fit">GitHub repository</button>
                                </Link>
                            </div>
                        </div>
                    </div>
                )}
                <PopularImages />
            </div>
            <div>
                <PopularCategories />
                <div className="h-0.5 w-full my-4 rounded-full bg-neutral-100"></div>
                <div>
                    <div className="font-bold text-neutral-800">Donations</div>
                    <p className="text-xs text-neutral-400">
                        If you like the project, please consider making a
                        donation to help me mantain it!
                    </p>
                    <div className="my-2 flex flex-row items-center gap-2 w-full">
                        <div className="flex-1 h-2 rounded-full bg-neutral-200 overflow-hidden relative">
                            <div className="h-2 rounded-full bg-crayola-300 w-[27.97%]"></div>
                        </div>
                        <div className="text-xs text-neutral-800 leading-none">
                            $4.5
                        </div>
                    </div>
                    <div className="flex flex-row flex-wrap text-neutral-400 gap-1 leading-none text-xs">
                        <Link
                            href="https://patreon.com/nekidev"
                            target="_blank"
                            className="hover:underline"
                        >
                            Patreon
                        </Link>{" "}
                        &middot;
                        <Link
                            href="https://ko-fi.com/nekidev"
                            target="_blank"
                            className="hover:underline"
                        >
                            Ko-fi
                        </Link>{" "}
                        &middot;
                        <Link
                            href="https://buymeacoffee.com/nekidev"
                            target="_blank"
                            className="hover:underline"
                        >
                            Buy Me A Coffee
                        </Link>
                    </div>
                </div>
                <div className="h-0.5 w-full my-4 rounded-full bg-neutral-100"></div>
                <div className="flex flex-row flex-wrap text-neutral-400 gap-1 leading-none text-xs">
                    <Link
                        href="https://docs.nekosapi.com"
                        className="hover:underline"
                    >
                        API
                    </Link>{" "}
                    &middot;
                    <Link
                        href="https://discord.gg/b9Fv3kEfXc"
                        className="hover:underline"
                    >
                        Discord
                    </Link>{" "}
                    &middot;
                    <Link
                        href="https://github.com/Nekos-API/Nekos-API"
                        className="hover:underline"
                    >
                        GitHub
                    </Link>{" "}
                    &middot;
                    <Link href="/terms-of-use" className="hover:underline">
                        Terms of Use
                    </Link>{" "}
                    &middot;
                    <Link href="/privacy-policy" className="hover:underline">
                        Privacy Policy
                    </Link>{" "}
                    &middot;
                    <Link href="/about" className="hover:underline">
                        About
                    </Link>
                </div>
            </div>
        </div>
    );
}

function PopularImages() {
    const { data, error, isLoading } = useSWR(
        "/images?include=uploader&page[limit]=8&filter[ageRating]=sfw",
        fetcher
    );

    React.useEffect(() => {
        if (isLoading == false) {
            const c = new colcade("." + styles.imgsGrid, {
                columns: "." + styles.imgsGridCol,
                items: ".image",
            });
        }
    }, [data]);

    return (
        <div className="">
            <h3 className="text-2xl font-extrabold text-neutral-800">
                Popular images
            </h3>
            <div className="relative pt-4 max-w-full">
                <div className={styles.imgsGrid}>
                    {isLoading ? (
                        <></>
                    ) : error ? (
                        <div>Error</div>
                    ) : (
                        <>
                            <div className={`${styles.imgsGridCol} imgs-grid-col--1`}></div>
                            <div className={`${styles.imgsGridCol} imgs-grid-col--2`}></div>
                            <div className={`${styles.imgsGridCol} imgs-grid-col--3 hidden sm:block`}></div>
                            <div className={`${styles.imgsGridCol} imgs-grid-col--4 hidden lg:block`}></div>
                            {data.data.map((value, index) => {
                                return (
                                    <ImageComponent
                                        id={value.id}
                                        attributes={value.attributes}
                                        relationships={value.relationships}
                                        included={data.included}
                                    />
                                );
                            })}
                        </>
                    )}
                </div>
            </div>
            <div className="flex flex-col items-center justify-center">
                {isLoading && (
                    <div className="h-5 w-5 border-2 border-crayola-350 rounded-full animate-spin border-t-white my-2 break-inside-avoid-column"></div>
                )}
            </div>
            <div className="flex flex-col items-center gap-2 text-center mt-8">
                <div className="font-extrabold">Still looking for more?</div>
                <div className="flex flex-row items-center gap-2">
                    <LightPrimaryButton>Explore</LightPrimaryButton>
                    <ScaleBorderButton>Upload</ScaleBorderButton>
                </div>
            </div>
        </div>
    );
}

function ImageComponent({
    id,
    attributes: { file, title },
    relationships: { uploader },
    included,
}) {
    const included_uploader = included.filter((value, index) => {
        return value.type == "user" && value.id == uploader.data.id;
    })[0];
    return (
        <div className="image flex flex-col gap-2 relative break-inside-avoid-column group cursor-pointer mb-8">
            <img
                src={file}
                className="border border-neutral-200 rounded-lg w-full transition-all drop-shadow-none group-hover:drop-shadow"
            />
            <div className="leading-none line-clamp-1 font-bold transition-colors group-hover:text-crayola-350">
                {title}
            </div>
            <div className="flex flex-row items-center gap-2">
                <img
                    src={included_uploader.attributes.avatarImage}
                    className="h-6 w-6 rounded-full border-2 border-neutral-200"
                />
                <div className="text-sm font-medium">
                    {included_uploader.attributes.username}
                </div>
            </div>
        </div>
    );
}

function PopularCategories() {
    const { data, error, isLoading } = useSWR("/categories", fetcher);

    return (
        <div>
            <h5 className="text-xl font-extrabold">Popular categories</h5>
            <div className="mt-2 flex flex-col gap-0 items-center">
                {isLoading ? (
                    <div className="h-5 w-5 border-2 border-crayola-350 rounded-full animate-spin border-t-white my-2"></div>
                ) : error ? (
                    <div>Error</div>
                ) : (
                    data.data.map((value, index) => {
                        return (
                            <Link
                                href={"/category/" + value.id}
                                className="py-1 rounded-full w-full flex flex-row items-center justify-between transition relative group"
                            >
                                <div className="absolute top-0 bottom-0 -left-4 -right-4 rounded-full bg-crayola-50 opacity-0 scale-50 group-hover:scale-100 group-hover:opacity-100 transition-all"></div>
                                <div className="flex flex-row items-center gap-2">
                                    <HashtagIcon className="h-4 w-4 z-10 relative transition-colors group-hover:stroke-crayola-350" />
                                    <div className="relative z-10 transition-colors group-hover:text-crayola-350">
                                        {value.attributes.name}
                                    </div>
                                </div>
                                <div className="relative overflow-hidden flex flex-col h-4 items-end">
                                    <div className="text-neutral-400 text-sm flex flex-row items-center gap-2 group-hover:-mt-4 transition-all h-4">
                                        3.5k
                                        <HeartIcon className="h-4 w-4" />
                                    </div>
                                    <ArrowRightIcon className="h-4 w-4 stroke-crayola-350 -mb-4 transition-all group-hover:mb-0" />
                                </div>
                            </Link>
                        );
                    })
                )}
            </div>
            <Link
                href="/category"
                className="flex flex-row items-center gap-2 text-crayola-350 mt-2 group"
            >
                <div className="underline decoration-crayola-150 group-hover:decoration-crayola-300 transition-colors underline-offset-4 text-sm">
                    See more
                </div>
                <ArrowRightIcon className="h-3 w-3 mt-1" />
            </Link>
        </div>
    );
}
