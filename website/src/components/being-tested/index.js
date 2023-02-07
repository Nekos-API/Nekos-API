"use client"

import { LightPrimaryButton } from "@/components/button";
import { ArrowLeftIcon } from "@heroicons/react/24/outline";
import { useRouter } from "next/navigation";

export default function BeingTested() {
    const router = useRouter();

    return (
        <div className="absolute top-0 left-0 right-0 h-screen flex flex-col items-center justify-center">
            <h1 className="text-4xl font-extrabold text-neutral-800">This feature is not available yet</h1>
            <p className="text-neutral-500 mt-2">The new version is still being tested, and therefore we cannot enable all features at once.</p>
            <div className="mt-8">
                <LightPrimaryButton onClick={() => {
                    router.back();
                }}>
                    <div className="flex flex-row items-center gap-2">
                        <ArrowLeftIcon className="h-5 w-5" />
                        Go back
                    </div>
                </LightPrimaryButton>
            </div>
        </div>
    )
}