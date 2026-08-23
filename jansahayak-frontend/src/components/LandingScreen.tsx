import { SetStateAction } from "react";
import PromptBar from "./PromptBar";
import { Msg } from "./chatting/ChatInterface";
import { Chat } from "./SideBar"
import Image from "next/image";

interface Props {
    setNewMessage: React.Dispatch<SetStateAction<Msg | null>>
    setCurrentChat: React.Dispatch<SetStateAction<{ _id: string; title: string; } | null>>,
    currentChat: { _id: string; title: string; } | null,
    setChats: React.Dispatch<SetStateAction<Chat[] | null>>,
}

export default function LandingScreen({ setNewMessage, setCurrentChat, currentChat, setChats }: Props) {
    return (
        <div className="ml-0 md:ml-55 flex flex-col items-center gap-10">
            {/* Heading and Slogan */}
            <div className="text-center">
                <div className="relative w-50 h-50 m-auto">
                    <Image
                        src="/Jansahayak-Logo.png"
                        alt="Jansahayak Logo"
                        fill
                        className="object-cover opacity-80"
                    />
                </div>
                <h1 className="text-xl md:text-4xl font-bold text-black">JANSAHAYAK</h1>
                <p className="text-texts-secondary text-xs md:text-sm italic"> Feding India With Knowledge</p>
            </div>
            <div className="relative group">
                {/* Large Soft Fading Shadow Layer (Lighter Indigo & Higher Blur) */}
                <div className="absolute -inset-3 rounded-full overflow-hidden pointer-events-none blur-3xl opacity-70 group-hover:opacity-90 transition-opacity duration-300">
                    <div className="absolute inset-[-160%] animate-[spin_7s_linear_infinite] bg-[conic-gradient(from_0deg,#f97316cc_0%,#ffffff_25%,#818cf8a6_35%,#ffffff_45%,#22c55ecc_75%,#f97316cc_100%)]" />
                </div>

                {/* Inner Tight Border Glow Layer */}
                <div className="relative rounded-full overflow-hidden p-0.5">
                    <div className="absolute inset-[-150%] animate-[spin_5s_linear_infinite] bg-[conic-gradient(from_0deg,#f97316cc_0%,#ffffff_25%,#6366f1e6_35%,#ffffff_45%,#22c55ecc_75%,#f97316cc_100%)] blur-md opacity-80 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />

                    {/* Main Outer Container */}
                    <PromptBar setNewMessage={setNewMessage} setCurrentChat={setCurrentChat} currentChat={currentChat} setChats={setChats} />
                </div>
            </div>
        </div>
    )
}