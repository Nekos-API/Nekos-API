"use client";

import { LightPrimaryButton, TextButton } from "@/components/button";
import Auth from "@/utils/authorization";
import { ExclamationCircleIcon, PencilIcon } from "@heroicons/react/24/outline";
import React from "react";

export default function CreateApplication() {
    const [isSaving, setIsSaving] = React.useState(false);

    const iconImageInputRef = React.useRef();
    const nameInputRef = React.useRef();
    const descriptionInputRef = React.useRef();
    const redirectUrisInputRef = React.useRef();
    const clientTypeInputRef = React.useRef();

    const [selectedImage, setSelectedImage] = React.useState();

    const [createdApplicationData, setCreatedApplicationData] =
        React.useState();

    const imageChange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            setSelectedImage(e.target.files[0]);
        }
    };

    return (
        <div className="flex flex-col gap-6 text-sm relative">
            {!createdApplicationData ? (
                <>
                    <h2 className="text-3xl font-extrabold">
                        Create an application
                    </h2>
                    <div className="flex flex-row items-start gap-6">
                        <div className="flex-1 relative flex flex-col gap-6">
                            <div className="flex flex-col gap-1">
                                <span className="font-bold">Name</span>
                                <input
                                    type="text"
                                    className="px-3 py-2 leading-none border-2 border-neutral-200 w-full rounded-md outline-none focus:ring-4 focus:ring-crayola-100 focus:border-crayola-300 transition-all"
                                    ref={nameInputRef}
                                    placeholder="My super exiting application"
                                />
                                <p className="text-xs text-neutral-500">
                                    What's your application's name? This will be
                                    shown to the users at the authorization
                                    page.
                                </p>
                            </div>
                            <div className="flex flex-col gap-1">
                                <span className="font-bold block">
                                    Description
                                </span>
                                <textarea
                                    type="text"
                                    className="w-full outline-none p-3 rounded-md border-2 border-neutral-200 focus:ring-4 focus:ring-crayola-100 focus:border-crayola-300 transition resize-y"
                                    placeholder={
                                        "The best application to login with Nekos API."
                                    }
                                    ref={descriptionInputRef}
                                ></textarea>
                                <p className="text-xs text-neutral-500">
                                    What is your application about? Write a
                                    short description so that users know where
                                    they're logging in.
                                </p>
                            </div>
                            <div className="flex flex-col gap-1">
                                <span className="font-bold block">
                                    Redirect URIs
                                </span>
                                <textarea
                                    type="text"
                                    className="w-full outline-none p-3 rounded-md border-2 border-neutral-200 focus:ring-4 focus:ring-crayola-100 focus:border-crayola-300 transition resize-y"
                                    rows={4}
                                    placeholder={
                                        "A list of all callback URIs to where your users will be redirected after authorization, delimited by a space. For example:\n\nhttps://example.com/login/callback https://different.example.com/login/callback"
                                    }
                                    ref={redirectUrisInputRef}
                                ></textarea>
                                <p className="text-xs text-neutral-500">
                                    Where should users be redirected to after
                                    they authorize (or not) your application?
                                    This is where the authorization code will be
                                    sent.
                                </p>
                            </div>
                            <div className="flex flex-col gap-1">
                                <span className="font-bold block">
                                    Client type
                                </span>
                                <select className="px-3 py-2 leading-none border-2 border-neutral-200 w-full rounded-md outline-none focus:ring-4 focus:ring-crayola-100 focus:border-crayola-300 transition-all">
                                    <option
                                        selected={true}
                                        value="confidential"
                                        ref={clientTypeInputRef}
                                    >
                                        Confidential
                                    </option>
                                    <option value="public">Public</option>
                                </select>
                                <p className="text-xs text-neutral-500">
                                    Can you store your client credentials
                                    securely? If you can, select{" "}
                                    <b>Confidential</b>. Otherwise, set{" "}
                                    <b>Public</b>.
                                </p>
                            </div>
                            <div className="flex flex-row items-center gap-3">
                                <div>
                                    <LightPrimaryButton
                                        onClick={() => {
                                            let name =
                                                nameInputRef.current.value;
                                            let description =
                                                descriptionInputRef.current
                                                    .value;
                                            let redirectUris =
                                                redirectUrisInputRef.current
                                                    .value;
                                            let clientType =
                                                clientTypeInputRef.current
                                                    .value;
                                            let icon = selectedImage;

                                            if (name.length < 4) {
                                                alert(
                                                    "The name must be at least 4 characters long."
                                                );
                                                return;
                                            } else if (name.length > 32) {
                                                alert(
                                                    "That name is too long! Max 32 characters are permitted."
                                                );
                                                return;
                                            } else if (
                                                description.length < 30
                                            ) {
                                                alert(
                                                    "Lets see what is this application about... Wait, it has no description! Seems suspicious, doesn't it? Add a description so that users know who they're sharing their information with (at least 30 characters long)!"
                                                );
                                                return;
                                            } else if (
                                                description.length > 500
                                            ) {
                                                alert(
                                                    "Lets see what is this application about... Too much text, better not signing in... Did you really write a description with +500 characters? Make it shorter or users will go away!"
                                                );
                                                return;
                                            } else if (
                                                // Thats the shortest url in the world. Any shorter than that is obviously invalid.
                                                redirectUris.length <
                                                "http://a.tk/".length
                                            ) {
                                                alert(
                                                    "Where are your users going to be redirected if you don't specify it? They'll stay in the authorization form forever and never come back. There you go, one user less. Specify at least one valid URL to redirect your users!"
                                                );
                                                return;
                                            }

                                            setIsSaving(true);
                                            fetch(
                                                process.env
                                                    .NEXT_PUBLIC_API_BASE +
                                                    "/applications",
                                                {
                                                    method: "POST",
                                                    credentials: "include",
                                                    headers: {
                                                        Accept: "application/vnd.api+json",
                                                        "Content-Type":
                                                            "application/vnd.api+json",
                                                    },
                                                    body: JSON.stringify({
                                                        data: {
                                                            type: "application",
                                                            attributes: {
                                                                name: name,
                                                                description:
                                                                    description,
                                                                redirectUris:
                                                                    redirectUris,
                                                                authorizationGrantType:
                                                                    "authorization-code",
                                                                clientType:
                                                                    clientType,
                                                            },
                                                        },
                                                    }),
                                                }
                                            )
                                                .then((data) => data.json())
                                                .then((data) => {
                                                    if (data.errors) {
                                                        alert(
                                                            "An error occurred when updating your profile info."
                                                        );
                                                    } else {
                                                        var body =
                                                            new FormData();
                                                        body.append(
                                                            "file",
                                                            icon
                                                        );

                                                        fetch(
                                                            process.env
                                                                .NEXT_PUBLIC_API_BASE +
                                                                `/applications/${data.data.id}/icon`,
                                                            {
                                                                method: "PUT",
                                                                credentials:
                                                                    "include",
                                                                headers: {
                                                                    Accept: "application/vnd.api+json",
                                                                },
                                                                body: body,
                                                            }
                                                        )
                                                            .then((res) => {
                                                                setCreatedApplicationData(
                                                                    data.data
                                                                );
                                                                if (
                                                                    res.status ==
                                                                    204
                                                                ) {
                                                                    alert(
                                                                        "The application was created successfully!"
                                                                    );
                                                                } else {
                                                                    alert(
                                                                        "The application was created, but the image could not be uploaded. Check that the format is supported and that the image is max 4 MB."
                                                                    );
                                                                }
                                                                setIsSaving(
                                                                    false
                                                                );
                                                            })
                                                            .catch((err) => {
                                                                alert(
                                                                    "The application was created successfully, but an unknown error prevented the image from uploading. Try again later."
                                                                );
                                                                setIsSaving(
                                                                    false
                                                                );
                                                            });
                                                    }
                                                })
                                                .catch((err) => {
                                                    alert(
                                                        "An unknown error occurred!"
                                                    );
                                                    setIsSaving(false);
                                                });
                                        }}
                                    >
                                        <div className="relative">
                                            {isSaving ? (
                                                <>
                                                    <div className="opacity-0">
                                                        Create
                                                    </div>
                                                    <div className="absolute top-0 bottom-0 left-0 right-0 m-auto h-5 w-5 border-2 border-crayola-350 border-t-transparent rounded-full animate-spin"></div>
                                                </>
                                            ) : (
                                                <>Create</>
                                            )}
                                        </div>
                                    </LightPrimaryButton>
                                </div>
                            </div>
                        </div>
                        <div className="h-36 w-36 rounded-full border-2 border-neutral-200 overflow-hidden relative">
                            <img
                                className="h-full w-full object-cover"
                                style={{
                                    display: selectedImage ? "block" : "none",
                                }}
                                src={
                                    selectedImage &&
                                    URL.createObjectURL(selectedImage)
                                }
                            />
                            <div className="h-full w-full flex flex-col justify-center items-center text-center bg-neutral-100 p-2">
                                Upload an application icon (max 4 MB).
                            </div>
                            <div
                                className="h-full w-full top-0 bottom-0 left-0 right-0 absolute bg-transparent hover:bg-black/60 transition cursor-pointer group flex flex-col items-center justify-center"
                                onClick={() => {
                                    iconImageInputRef.current.click();
                                }}
                            >
                                <PencilIcon className="h-8 w-8 stroke-white scale-50 opacity-0 group-hover:scale-100 group-hover:opacity-100 transition-all" />
                            </div>
                            <input
                                type="file"
                                ref={iconImageInputRef}
                                onChangeCapture={imageChange}
                                accept="image/*"
                            />
                        </div>
                    </div>
                </>
            ) : (
                <>
                    <h2 className="text-3xl font-extrabold">
                        {createdApplicationData.attributes.name}
                    </h2>
                    <div className="flex flex-row gap-4 p-4 rounded-lg border-2 border-neutral-200 bg-neutral-100">
                        <ExclamationCircleIcon className="h-6 w-6" />
                        <div className="flex flex-col gap-2 flex-1">
                            <div className="font-bold text-base">
                                Save your credentials now!
                            </div>
                            <p>
                                Store both client ID and client secret now. You
                                will not be able to see the secret again. If you
                                lose it, that means that your application is
                                lost forever (well, if you somehow can contact
                                god then he may give you another secret, but I
                                wouldn't reccommend trying it).
                            </p>
                        </div>
                    </div>
                    <div className="flex flex-col items-start gap-6">
                        <div>
                            <div className="text-xl font-bold">Client ID</div>
                            <div className="text-base break-all font-mono">
                                {
                                    createdApplicationData.attributes
                                        .credentials.clientId
                                }
                            </div>
                        </div>
                        <div>
                            <div className="text-xl font-bold">
                                Client Secret
                            </div>
                            <div className="text-base break-all font-mono">
                                {
                                    createdApplicationData.attributes
                                        .credentials.clientSecret
                                }
                            </div>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
}
