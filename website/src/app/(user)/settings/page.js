"use client";

import { useRouter } from "next/navigation";

export default function SettingsRedirect() {
    const router = useRouter();
    router.push("/settings/profile");
    return (
        <div className="w-full h-96 flex flex-col items-center justify-center">
            <div className="h-6 w-6 rounded-full border-2 border-crayola-350 border-t-transparent animate-spin"></div>
        </div>
    );
}
