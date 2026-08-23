import api from "@/lib/axiosInstance";
import { handleAxiosError } from "@/utils/handleError";
import Link from "next/link";
import { useRouter } from "next/navigation";
import React, { SetStateAction, useLayoutEffect, useState } from "react"
import { LuArrowRight, LuChevronRight, LuEllipsisVertical, LuLogOut, LuSettings, LuStar, LuUser } from "react-icons/lu";
import SignOutPrompter from "./SignoutPrompter";

export interface Chat {
    _id: string,
    title: string
}
interface User {
    _id: string,
    name: {
        first: string,
        last: string
    }
    email: string,
    occupation: string
}

interface SideBarProps {
    sideBarRef: React.RefObject<HTMLDivElement | null>
    setCurrentChat: React.Dispatch<SetStateAction<Chat | null>>
    currentChat: Chat | null
    chats: Chat[] | null
    setChats: React.Dispatch<SetStateAction<Chat[] | null>>
}

const SideBar = ({ sideBarRef, setCurrentChat, currentChat, chats, setChats }: SideBarProps) => {
    const [user, setUser] = useState<User | null>(null);
    const [signOutPromptOpen, setSignOutPromptOpen] = useState<boolean>(false);
    const [profileClickOptions, setProfileClickOptions] = useState<boolean>(false);

    const fetchMyDetails = async () => {
        try {
            const response = await api.get("/profiles/myDetails");
            if (response.data) {
                setUser(response.data.profile || null);
            }
        } catch (error) {
            console.error(handleAxiosError(error));
        }
    };

    const fetchAllChats = async () => {
        try {
            const response = await api.get("/chats");
            if (!response.data || !response.data.success) throw new Error();
            setChats(response.data.chats)
        } catch (error) {
            console.error(handleAxiosError(error))
        }
    }
    useLayoutEffect(() => {
        fetchMyDetails();
        fetchAllChats();
        return () => {
            sideBarRef.current = null
        };
    }, [])

    return (
        <>
            {signOutPromptOpen && <SignOutPrompter setSignoutPromptOpen={setSignOutPromptOpen} />}
            <aside
                className={`sidebar sidebar-open z-800 fixed w-68 left-0 px-5 py-10 md:h-screen md:py-5 flex flex-col justify-start bg-ui-background overflow-x-clip border-r border-ui-tertiary/20 shadow-2xl shadow-black/50`}
                ref={sideBarRef}
            >
                {/* Logo and Name */}
                <div className="flex items-center justify-start gap-2.5 w-fit px-2 py-2 mb-4 text-texts-dark rounded-full font-bold text-md md:text-xl tracking-wide">
                    <img src="/Jansahayak-Logo.png" alt="Logo" width={50} height={50} className="rounded-full" />
                    JANSAHAYAK
                </div>
                {
                    !user &&
                    <>
                        <Link href="/auth" className="flex flex-row gap-2 items-center border border-ui-tertiary/20 shadow-sm shadow-black/20 py-2 px-2.5 w-fit rounded-full justify-center hover:bg-ui-tertiary/30 transition-colors duration-100 cursor-pointer">
                            <span className="border border-ui-tertiary/20 bg-ui-tertiary/40 shadow-sm shadow-black/20 rounded-full p-2.5">
                                <LuUser size={16} className="text-texts-dark" />
                            </span>
                            <span
                                className="text-texts-dark"
                            >
                                SignIn / SignUp
                            </span>
                            <LuChevronRight size={16} className="text-texts-dark" />
                        </Link>

                        <Link href="/privacypolicy" className="text-indigo-400 font-semibold focus-visible:underline text-sm md:text-md mt-5 flex items-center gap-2 ml-2 hover:scale-101">
                            Privacy Policy <LuArrowRight size={16} />
                        </Link>
                    </>
                }

                {/* Main */}
                <section className="relative text-texts-dark overflow-y-scroll scrollbar-thumb-ui-tertiary scrollbar-thin h-140">
                    {/* Chats */}
                    <div className="flex flex-col text-sm md:text-md gap-1">
                        {chats?.map((chat) => (
                            <div
                                className={`${currentChat?._id === chat._id ? "bg-ui-tertiary/60" : ""} py-2 px-4 flex items-center justify-between cursor-pointer truncate text-ellipsis hover:bg-ui-tertiary/50 rounded-3xl group transition-colors duration-150`}
                                key={chat._id}
                                onClick={() => { setCurrentChat((prev) => prev?._id == chat._id ? null : chat) }}
                                onTouchStart={() => { setCurrentChat((prev) => prev?._id == chat._id ? null : chat) }}
                            >
                                &bull; &nbsp;{chat.title} <LuEllipsisVertical size={16} className="opacity-0 group-hover:opacity-80 hover:bg-ui-tertiary rounded-full p-0.5" />
                            </div>
                        ))}
                    </div>
                </section>
                {
                    user &&
                    <Link
                        href="#"
                        className="realtive flex flex-row mb-8 md:mb-0 md:mt-4 gap-2 items-center border border-ui-tertiary/20 shadow-sm shadow-black/20 py-2 px-2.5 w-fit rounded-full justify-center hover:bg-ui-tertiary/30 transition-colors duration-100 cursor-pointer"
                        onClick={() => setProfileClickOptions(prev => !prev)}
                    >
                        {
                            profileClickOptions &&
                            <div
                                onClick={(e) => { setSignOutPromptOpen(true) }}
                                onMouseLeave={() => setProfileClickOptions(false)}
                                className="bg-ui-background absolute rounded-3xl bottom-22 left-8 shadow-black/40 shadow-sm px-4 py-3 flex items-center gap-2 text-texts-dark/80 hover:bg-ui-tertiary/70 transition-colors cursor-pointer duration-100"
                            >
                                SignOut <LuLogOut size={13} />
                            </div>
                        }

                        <span className="border border-ui-tertiary/20 bg-ui-tertiary/40 shadow-sm shadow-black/20 rounded-full p-2.5">
                            <LuUser size={16} className="text-texts-dark" />
                        </span>
                        <span
                            className="text-texts-dark"
                        >
                            {user.name?.first + " " + user.name?.last}
                        </span>
                        <LuChevronRight size={16} className="text-texts-dark" />
                    </Link>
                }
                <button className="fixed left-55 md:left-56 md:left-52 bottom-20 md:bottom-7 text-sm md:text-lg bg-buttons hover:bg-buttons/70 transition-colors duration-100 rounded-full p-2">
                    <LuSettings size={20} />
                </button>
            </aside>
        </>
    )
}

export default SideBar;