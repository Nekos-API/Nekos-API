"use client";

import { LightPrimaryButton, TextButton } from "@/components/button";
import Auth from "@/utils/authorization";
import { PencilIcon } from "@heroicons/react/24/outline";
import React from "react";

export default function ProfileSettings() {
    const auth = new Auth();

    const { user, error, isLoading } = auth.useUser();

    const [isSaving, setIsSaving] = React.useState(false);
    const [isAvatarSaving, setIsAvatarSaving] = React.useState(false);

    const avatarImageInputRef = React.useRef();
    const usernameInputRef = React.useRef();
    const nicknameInputRef = React.useRef();
    const biographyInputRef = React.useRef();

    const [selectedImage, setSelectedImage] = React.useState();

    const imageChange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            setSelectedImage(e.target.files[0]);
        }
    };

    return (
        <div className="flex flex-col gap-6 text-sm relative">
            <h2 className="text-3xl font-extrabold">Profile</h2>
            <div className="flex flex-row items-start gap-6">
                <div className="flex-1 relative flex flex-col gap-6">
                    <div className="flex flex-col gap-1">
                        <span className="font-bold">Username</span>
                        <input
                            type="text"
                            className="px-3 py-2 leading-none border-2 border-neutral-200 w-full rounded-md outline-none focus:ring-4 focus:ring-crayola-100 focus:border-crayola-300 transition-all"
                            defaultValue={user && user.attributes.username}
                            ref={usernameInputRef}
                        />
                        <p className="text-xs text-neutral-500">
                            This will be used in your profile url. Your username
                            needs to be unique, so select the one you like
                            before other user grabs it!
                        </p>
                    </div>
                    <div className="flex flex-col gap-1">
                        <span className="font-bold block">Nickname</span>
                        <input
                            type="text"
                            className="px-3 py-2 leading-none border-2 border-neutral-200 w-full rounded-md outline-none focus:ring-4 focus:ring-crayola-100 focus:border-crayola-300 transition-all placeholder:text-neutral-400"
                            placeholder={user && user.attributes.username}
                            defaultValue={user && user.attributes.nickname}
                            ref={nicknameInputRef}
                        />
                        <p className="text-xs text-neutral-500">
                            This is the name that will be displayed everywhere.
                            Your username will be shown below your nickname to
                            diferentiate users with the same nickname.
                        </p>
                    </div>
                    <div className="flex flex-col gap-1">
                        <span className="font-bold block">Biography</span>
                        <textarea
                            type="text"
                            className="w-full outline-none p-3 rounded-md border-2 border-neutral-200 focus:ring-4 focus:ring-crayola-100 focus:border-crayola-300 transition resize-y"
                            placeholder={
                                user &&
                                `Hi! I'm ${user.attributes.username}, a catgirl lover that...`
                            }
                            defaultValue={user && user.attributes.biography}
                            ref={biographyInputRef}
                        ></textarea>
                        <p className="text-xs text-neutral-500">
                            Tell us a bit about yourself. Who are you? What do
                            you like doing? Which is your favorite waifu?
                        </p>
                    </div>
                    <div className="flex flex-row items-center gap-3">
                        <div>
                            <LightPrimaryButton
                                onClick={() => {
                                    let username =
                                        usernameInputRef.current.value;
                                    let nickname =
                                        nicknameInputRef.current.value;
                                    let biography =
                                        biographyInputRef.current.value;
                                    let avatar = selectedImage;

                                    if (username.length < 4) {
                                        alert(
                                            "The username must be at least 4 characters long."
                                        );
                                        return;
                                    } else if (username.length > 16) {
                                        alert(
                                            "That username is too long! Max 16 characters are permitted."
                                        );
                                        return;
                                    }

                                    if (
                                        username.toString() != user.attributes.username ||
                                        nickname.toString() != user.attributes.nickname ||
                                        biography.toString() != user.attributes.biography
                                    ) {
                                        setIsSaving(true);
                                        fetch(
                                            process.env.NEXT_PUBLIC_API_BASE +
                                                "/users/" +
                                                user.id,
                                            {
                                                method: "PATCH",
                                                credentials: "include",
                                                headers: {
                                                    Accept: "application/vnd.api+json",
                                                    "Content-Type":
                                                        "application/vnd.api+json",
                                                },
                                                body: JSON.stringify({
                                                    data: {
                                                        type: "user",
                                                        id: user.id,
                                                        attributes: {
                                                            username: username,
                                                            nickname: nickname,
                                                            biography:
                                                                biography,
                                                        },
                                                    },
                                                }),
                                            }
                                        )
                                            .then((data) => data.json())
                                            .then((data) => {
                                                setIsSaving(false);
                                                if (data.errors) {
                                                    alert(
                                                        "An error occurred when updating your profile info."
                                                    );
                                                } else {
                                                    alert(
                                                        "Your profile info was updated successfully!"
                                                    );
                                                }
                                                auth.update();
                                            }).catch((err) => {
                                                alert("An unknown error occurred!")
                                                setIsSaving(false);
                                            });
                                    }

                                    if (avatar) {
                                        setIsAvatarSaving(true);

                                        var data = new FormData();
                                        data.append("file", avatar);

                                        fetch(
                                            process.env.NEXT_PUBLIC_API_BASE +
                                                "/users/@me/avatar",
                                            {
                                                method: "PUT",
                                                credentials: "include",
                                                headers: {
                                                    Accept: "application/vnd.api+json",
                                                },
                                                body: data,
                                            }
                                        )
                                            .then((data) => {
                                                if (data.status == 204) {
                                                    alert(
                                                        "Your profile image was updated successfully!"
                                                    );
                                                } else {
                                                    alert(
                                                        "Oops! Your profile image could not be uploaded. Check that the format is supported (png, jpeg, webp, jfif, avif, bmp) and try again."
                                                    );
                                                }
                                                auth.update();
                                                setIsAvatarSaving(false);
                                            })
                                            .catch((err) => {
                                                setIsAvatarSaving(false);
                                                alert(
                                                    "An unknown error occurred."
                                                );
                                            });
                                    }
                                }}
                            >
                                <div className="relative">
                                    {isSaving || isAvatarSaving ? (
                                        <>
                                            <div className="opacity-0">
                                                Save
                                            </div>
                                            <div className="absolute top-0 bottom-0 left-0 right-0 m-auto h-5 w-5 border-2 border-crayola-350 border-t-transparent rounded-full animate-spin"></div>
                                        </>
                                    ) : (
                                        <>Save</>
                                    )}
                                </div>
                            </LightPrimaryButton>
                        </div>
                        <div>
                            <TextButton
                                onClick={() => {
                                    setSelectedImage();
                                    usernameInputRef.current.value =
                                        user.attributes.username;
                                    nicknameInputRef.current.value =
                                        user.attributes.nickname;
                                    biographyInputRef.current.value =
                                        user.attributes.biography;
                                }}
                            >
                                Discard changes
                            </TextButton>
                        </div>
                    </div>
                </div>
                <div className="h-36 w-36 rounded-full border-2 border-neutral-200 overflow-hidden relative">
                    {isLoading ? (
                        <div className="h-full w-full bg-neutral-200 animate-pulse"></div>
                    ) : error ? (
                        <div>Error</div>
                    ) : (
                        <>
                            <img
                                className="h-full w-full object-cover"
                                src={
                                    selectedImage
                                        ? URL.createObjectURL(selectedImage)
                                        : user.attributes.avatarImage
                                }
                            />
                            <div
                                className="h-full w-full top-0 bottom-0 left-0 right-0 absolute bg-transparent hover:bg-black/60 transition cursor-pointer group flex flex-col items-center justify-center"
                                onClick={() => {
                                    avatarImageInputRef.current.click();
                                }}
                            >
                                <PencilIcon className="h-8 w-8 stroke-white scale-50 opacity-0 group-hover:scale-100 group-hover:opacity-100 transition-all" />
                            </div>
                        </>
                    )}
                    <input
                        type="file"
                        ref={avatarImageInputRef}
                        onChangeCapture={imageChange}
                        accept="image/*"
                    />
                </div>
            </div>
        </div>
    );
}
