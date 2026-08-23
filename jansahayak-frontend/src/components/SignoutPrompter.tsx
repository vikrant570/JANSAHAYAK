"use client";
import { useToastMsgContext } from "@/contexts/ToastMsgContext";
import api from "@/lib/axiosInstance";
import { handleAxiosError } from "@/utils/handleError";
import { useRouter } from "next/router";

import { SetStateAction, useRef } from "react"

const SignOutPrompter = ({ setSignoutPromptOpen }: { setSignoutPromptOpen: React.Dispatch<SetStateAction<boolean>> }) => {
    const router = useRouter();
    const PromptBodyRef = useRef<HTMLDivElement | null>(null);
    const { showToastMsg } = useToastMsgContext();

    const handleSignOut = async () => {
        try {
            const response = await api.delete("/auth/signout");
            if (!response || !response.data || !response.data.success) throw new Error();
            setSignoutPromptOpen(false);
            router.reload();
        } catch (error) {
            showToastMsg({ text: handleAxiosError(error), type: "error" })
        }
    }

    const handleOutSideClick = (event: React.MouseEvent<HTMLDialogElement>) => {
        if (!PromptBodyRef.current?.contains(event.target as Node)) setSignoutPromptOpen(false);
    }

    return (
        <dialog open={true} onClick={handleOutSideClick} className="z-9999 absolute w-screen h-screen top-0 bg-texts-dark/10 backdrop-blur-xs">
            <div ref={PromptBodyRef} className="m-auto mt-60 w-1/4 py-4 rounded-3xl bg-ui-background flex flex-col items-center justify-center shadow-black/30 shadow-xl border-ui-tertiary border-3">
                <p className="text-texts-dark/80 text-lg font-semibold">Are you sure you want to sign out?</p>
                <img src={"/Jansahayak-Logo.png"} width={100} height={100} className="rounded-full" />
                <div className="flex justify-between w-1/2 mt-4">
                    <button onClick={() => setSignoutPromptOpen(false)} className="mr-2 px-4 py-2 bg-ui-tertiary/20 rounded-full hover:bg-ui-tertiary/50 transition-colors duration-100 cursor-pointer">Cancel</button>
                    <button onClick={handleSignOut} className="px-4 py-2 bg-red-500 text-white rounded-full hover:bg-red-400 transition-colors duration-100 cursor-pointer">Sign Out</button>
                </div>
            </div>
        </dialog>
    )
}

export default SignOutPrompter;