"use client";
import ChatInterface, { Msg } from "@/components/chatting/ChatInterface";
import LandingScreen from "@/components/LandingScreen";
import SideBar, { Chat } from "@/components/SideBar";
import { useEffect, useRef, useState } from "react";
import { FaBars } from "react-icons/fa";

export default function Home() {
  const [sideBarOpen, setSideBarOpen] = useState<boolean>(true);
  const [currentChat, setCurrentChat] = useState<{ _id: string, title: string } | null>(null);
  const [newMessage, setNewMessage] = useState<Msg | null>(null);
  const [chats, setChats] = useState<Chat[] | null>(null);

  const sideBarRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined" && window.innerWidth < 768) {
      setSideBarOpen(false);
    }
    import("eruda").then(e => e.default.init())
  }, []);

  const handleScreenClick = (e: any) => {
    if (window.innerWidth > 768) return;

    if (sideBarRef.current && !sideBarRef.current.contains(e.target)) {
      setSideBarOpen(false);
    }
  }

  return (
    <main className="flex flex-1 justify-center items-center bg-ui-background px-0 overflow-x-clip overflow-y-scroll h-screen" onTouchStart={handleScreenClick}>
      {
        !sideBarOpen &&
        <button
          className="bg-ui-background rounded-full p-3 w-11 h-11 text-black border border-ui-tertiary/10 shadow-sm shadow-black/10 inset-[10%] absolute top-8 left-5"
          onClick={() => { setSideBarOpen(true) }}
        >
          <FaBars size={20} />
        </button>
      }
      {sideBarOpen && <SideBar sideBarRef={sideBarRef} setCurrentChat={setCurrentChat} currentChat={currentChat} chats={chats} setChats={setChats} />}
      {/* Replace div with current chat */}
      {currentChat ?
        <ChatInterface chat={currentChat} setNewMessage={setNewMessage} newMessage={newMessage} setCurrentChat={setCurrentChat} setChats={setChats} />
        :
        <LandingScreen setNewMessage={setNewMessage} currentChat={currentChat} setCurrentChat={setCurrentChat} setChats={setChats} />}
    </main>
  );
}