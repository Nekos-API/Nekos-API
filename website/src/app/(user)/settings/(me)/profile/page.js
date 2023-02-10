"use client";

import { LightPrimaryButton, TextButton } from "@/components/button";
import Auth from "@/utils/authorization";
import { PencilIcon } from "@heroicons/react/24/outline";

export default function ProfileSettings() {
    const auth = new Auth();

    const { user, error, isLoading } = auth.useUser();

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
                            value={user && user.attributes.username}
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
                        ></textarea>
                        <p className="text-xs text-neutral-500">
                            Tell us a bit about yourself. Who are you? What do
                            you like doing? Which is your favorite waifu?
                        </p>
                    </div>
                    <div className="flex flex-row items-center gap-3">
                        <div>
                            <LightPrimaryButton>Save</LightPrimaryButton>
                        </div>
                        <div>
                            <TextButton>Discard changes</TextButton>
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
                                src={user.attributes.avatarImage}
                            />
                            <div className="h-full w-full top-0 bottom-0 left-0 right-0 absolute bg-transparent hover:bg-black/60 transition cursor-pointer group flex flex-col items-center justify-center">
                                <PencilIcon className="h-8 w-8 stroke-white scale-50 opacity-0 group-hover:scale-100 group-hover:opacity-100 transition-all" />
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}
