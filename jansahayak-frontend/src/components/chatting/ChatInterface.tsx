"use client"
import { useState, useEffect, useLayoutEffect, useRef, useCallback, SetStateAction } from "react";
import api from "@/lib/axiosInstance";
import PromptBar from "../PromptBar";
import Message from "./Message";
import { Chat } from "../SideBar";

export interface Msg {
    _id: string,
    chatID: string,
    role: string,
    content: string,
    createdAt: string
}
interface Res {
    success: boolean,
    messages: Msg[],
    hasMore: boolean,
    message?: string
}


interface ChatInterfaceProps {
    chat: {
        _id: string,
        title: string
    },
    setNewMessage: React.Dispatch<SetStateAction<Msg | null>>,
    newMessage: Msg | null,
    setCurrentChat: React.Dispatch<SetStateAction<{ _id: string; title: string; } | null>>,
    setChats: React.Dispatch<SetStateAction<Chat[] | null>>,
}

const ChatInterface = ({ chat, setNewMessage, newMessage, setCurrentChat, setChats }: ChatInterfaceProps) => {
    const chatID = chat._id;

    const [messages, setMessages] = useState<Msg[]>([]);
    const [cursor, setCursor] = useState<string>("");
    const [hasMore, setHasMore] = useState<boolean>(true);
    const [loading, setLoading] = useState<boolean>(false);

    // Element Refs
    const containerRef = useRef<HTMLDivElement | null>(null);
    const topSentinelRef = useRef<HTMLDivElement | null>(null);
    const bottomRef = useRef<HTMLDivElement | null>(null);

    // Logical Refs
    const prevScrollHeight = useRef<number>(0);
    const hasMoreRef = useRef<boolean>(hasMore);
    const loadingRef = useRef<boolean>(loading);

    // Syncing Refs With States
    useEffect(() => {
        hasMoreRef.current = hasMore;
        loadingRef.current = loading;
    }, [hasMore, loading]);

    // Scroll Helpers
    const scrollToBottom = () => {
        setTimeout(() => bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" }), 100);
    };

    const isNearBottom = (): boolean => {
        const el = containerRef.current;
        if (!el) return true;
        return el.scrollHeight - el.scrollTop - el.clientHeight < 150;
    };

    // Unified Message Fetch (Initial + Pagination)
    const fetchMessages = useCallback(async (paginationCursor: string, isInitial: boolean) => {
        if (!isInitial && !paginationCursor) return;

        try {
            setLoading(true);
            if (isInitial) {
                setMessages([]);
                setCursor("");
                setHasMore(true);
            }

            const res = await api.get(`/chats/${chatID}?cursor=${paginationCursor}`);
            if (!res.data.success && res.data.message === "Chat Doesn't Exist!") return;

            const msgs = (res.data as Res).messages;
            setMessages(prev => isInitial ? msgs : [...msgs, ...prev]);
            setHasMore(res.data.hasMore);
            if (msgs?.length > 0) setCursor(msgs[0]._id);
            if (isInitial) scrollToBottom();
        }
        catch (err) {
            console.error("Failed to fetch messages:", err);
        }
        finally {
            setLoading(false);
        }
    }, [chatID]);

    // Initial Fetch On Chat Change
    useEffect(() => {
        if (!chatID) return;
        fetchMessages("", true);
    }, [chatID, fetchMessages]);

    // Scroll Restoration After Pagination Prepend
    useLayoutEffect(() => {
        //Change in messages but not at the top
        if (messages[0]?._id == cursor) {
            bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
            setNewMessage(null);
            return;
        };

        // Change in messages but at the top
        if (prevScrollHeight.current > 0 && containerRef.current) {
            containerRef.current.scrollTop = containerRef.current.scrollHeight - prevScrollHeight.current;
            prevScrollHeight.current = 0;
        }
    }, [messages]);

    // Observer - Triggering Pagination
    useEffect(() => {
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !loadingRef.current && hasMoreRef.current) {
                prevScrollHeight.current = containerRef.current!.scrollHeight;
                fetchMessages(cursor, false);
            }
        }, {
            root: containerRef.current,
            threshold: 0
        });

        if (topSentinelRef.current) observer.observe(topSentinelRef.current);
        return () => { observer.disconnect() };
    }, [chatID, cursor, fetchMessages]);

    // Appending new messages to chat
    useEffect(() => {
        if (newMessage) {
            setMessages((prev) => [...prev, newMessage]);
        }
    }, [newMessage])

    return (
        <div className="ml-1.5 md:ml-70 h-full md:h-screen md:w-280 px-10 py-5 flex flex-col items-center bg-transparent">
            <span className="flex flex-row items-center text-xs">
                <p className="text-texts-dark/35"> <b>JANSAHAYAK</b> is an AI and can make mistakes &copy; 2026</p>
            </span>

            <div
                ref={containerRef}
                className="flex md:min-w-full flex-col gap-4 items-center h-[calc(100vh-8rem)] md:h-full pt-6 pb-1 overflow-y-scroll scroll-smooth scrollbar-none text-sm md:text-md"
            >
                {/* Top Sentinel - Triggers Pagination When Visible */}
                {hasMore && <div ref={topSentinelRef} className="h-1 w-full shrink-0" />}
                {loading && <p className="text-texts-secondary text-xs animate-pulse">Loading...</p>}

                {
                    messages.length > 0 ?
                        messages.map(message => (
                            <Message key={message._id} message={message} />
                        ))
                        :
                        !loading && <div className="text-texts-secondary">No messages yet</div>
                }

                {/* Bottom Sentinel - Scroll Anchor */}
                <div ref={bottomRef} className="h-1 w-full shrink-0" />
            </div>
            {/* Prompt Bar */}
            <PromptBar currentChat={chat} setNewMessage={setNewMessage} setCurrentChat={setCurrentChat} setChats={setChats} />
        </div>
    )
}
export default ChatInterface;
