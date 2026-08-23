"use client"
import { createContext, SetStateAction, useCallback, useContext, useRef, useState } from "react";

interface toastMsgInterface {
    text: string,
    type: "success" | "error" | "info"
}
//Context split to prevent uneccessary re-renders
interface toastMsgCtxInterface {
    ToastMsg: toastMsgInterface | null,
    showToastMsg: (toast: toastMsgInterface | null) => void
}

const ToastMsgContext = createContext<toastMsgCtxInterface | null>(null);

export const ToastMsgProvider = ({ children }: { children: React.ReactNode }) => {
    const [ToastMsg, setToastMsg] = useState<toastMsgInterface | null>(null);
    const coolDownTimer = useRef<NodeJS.Timeout | null>(null);

    // Preventing Render Flood For Too Many Errors
    const showToastMsg = useCallback((toast: toastMsgInterface | null) => {
        if (!toast) return;
        const { text, type } = toast;

        if (!coolDownTimer.current) {
            setToastMsg({ text, type });
            coolDownTimer.current = setTimeout(() => {
                setToastMsg(null);
                coolDownTimer.current = null;
            }, 4000)
        }
        return;
    }, []);

    return (
        <ToastMsgContext.Provider value={{ ToastMsg, showToastMsg }}>
            {children}
        </ToastMsgContext.Provider>
    )
}

// Value Context
export const useToastMsgContext = () => {
    const context = useContext(ToastMsgContext);

    if (!context) throw new Error("ToastMsg must be used within ToastMsgProvider");
    return context;
}