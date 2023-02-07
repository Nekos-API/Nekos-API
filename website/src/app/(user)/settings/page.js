"use client"

import { useRouter } from "next/navigation";

export default function SettingsRedirect() {
    const router = useRouter();
    router.push("/settings/profile");
    return <></>;
}