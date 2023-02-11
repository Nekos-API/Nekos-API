"use client";

import React from "react";

import { useRouter } from "next/navigation";

export default function Login() {
    const router = useRouter();
    router.push("https://sso.nekosapi.com/login?next=https://nekosapi.com")
    return <></>;
}
