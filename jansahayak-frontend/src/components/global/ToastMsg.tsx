"use client";
import { useToastMsgContext } from "@/contexts/ToastMsgContext";
import { LuX, LuCircleAlert, LuCircleCheck, LuInfo } from "react-icons/lu";
import { Activity, useEffect, useState } from "react";

export default function ToastNotification() {
    const { ToastMsg } = useToastMsgContext();
    const [isVisible, setIsVisible] = useState<boolean>(false);

    useEffect(() => {
        if (ToastMsg !== null) {
            setIsVisible(true);
        } else {
            setIsVisible(false);
        }
    }, [ToastMsg]);

    const type = ToastMsg?.type || 'error';
    const isInfo = type === 'info';
    const isSuccess = type === 'success';
    const isError = type === 'error';

    return (
        <Activity mode={isVisible && ToastMsg ? "visible" : "hidden"}>
            <div
                className={`fixed z-9999 transition-all duration-400 ease-out flex items-start ${isInfo ? 'bottom-15 left-1/2 -translate-x-1/2' : 'top-8 right-8'
                    } ${isVisible
                        ? (isInfo ? 'translate-y-0 opacity-100' : 'translate-y-0 translate-x-0 opacity-100')
                        : (isInfo ? 'translate-y-4 opacity-0 pointer-events-none' : '-translate-y-4 translate-x-4 opacity-0 pointer-events-none')
                    }`}
                onTouchStart={() => setIsVisible(false)}
            >
                {/* Main Toast Bubble */}
                <div
                    className={`flex items-center shadow-xl w-auto transition-colors text-shadow-black/20 text-shadow-sm ${isInfo
                        ? 'bg-ui-tertiary text-ui-main px-3 py-2 rounded-xl shadow-ui-tertiary/15 gap-2 max-w-sm'
                        : isSuccess
                            ? 'bg-green-500/90 text-texts-primary px-4 py-3 rounded-2xl shadow-green-500/10 gap-3 max-w-md'
                            : 'bg-red-500/90 text-texts-primary px-4 py-3 rounded-2xl shadow-red-600/10 gap-3 max-w-md'
                        }`}
                >
                    <div className={`shrink-0 p-1 rounded-full ${isError ? 'bg-texts-primary/20' : 'bg-ui-main/10'}`}>
                        {isSuccess && <LuCircleCheck size={16} className="text-ui-main" />}
                        {isError && <LuCircleAlert size={16} className="text-texts-primary/70" />}
                        {isInfo && <LuInfo size={14} className="text-ui-main" />}
                    </div>

                    <p className={`${isInfo ? 'text-sm' : 'text-sm'} font-semibold leading-snug pr-2`}>
                        {ToastMsg?.text}
                    </p>

                    <button
                        onClick={() => setIsVisible(false)}
                        className={`shrink-0 flex items-center justify-center rounded-full transition-colors ml-auto ${isError
                            ? 'bg-texts-primary/10 hover:bg-texts-primary/20 text-texts-primary w-6 h-6'
                            : isInfo
                                ? 'bg-ui-main/10 hover:bg-ui-main/20 text-ui-main w-5 h-5'
                                : 'bg-ui-main/10 hover:bg-ui-main/20 text-ui-main w-6 h-6'
                            }`}
                        aria-label="Dismiss message"
                    >
                        <LuX size={isInfo ? 12 : 14} />
                    </button>
                </div>
            </div>
        </Activity>
    )
}