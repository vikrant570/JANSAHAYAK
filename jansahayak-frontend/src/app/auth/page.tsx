"use client";
import { useState } from "react";
import SignInForm from "./components/SignInForm";
import SignUpForm from "./components/SignUpForm";
import OtpForm from "./components/OtpForm";
import { submitAuth, verifyOtp } from "@/lib/userGateway";
import type { SignInData, SignUpData, OtpData } from "@/types/authTypes";
import { useRouter } from "next/navigation";
import { useToastMsgContext } from "@/contexts/ToastMsgContext";
import { handleAxiosError } from "@/utils/handleError";

type Step = "form" | "otp";

const Authentication = () => {
    const [isUser, setIsUser] = useState<boolean>(true);
    const [step, setStep] = useState<Step>("form");
    const [email, setEmail] = useState("");
    const [loading, setLoading] = useState(false);
    const { showToastMsg } = useToastMsgContext();
    const router = useRouter();

    const handleAuthSubmit = async (data: SignInData | SignUpData) => {
        setLoading(true);
        try {
            const action = isUser ? "login" : "register";
            const res = await submitAuth(data, action);
            if (!res || !res.data.success) throw new Error();

            setEmail(data.email);
            setStep("otp");
        } catch (err) {
            showToastMsg({ text: handleAxiosError(err), type: "error" });
        } finally {
            setLoading(false);
        }
    };

    const handleOtpSubmit = async (data: OtpData) => {
        setLoading(true);
        try {
            const response = await verifyOtp(data, isUser ? "login" : "register");
            if (!response || !response.data.success) throw new Error();
            showToastMsg({ text: "OTP verification successful", type: "success" });
            router.push("/");
        } catch (err) {
            showToastMsg({ text: handleAxiosError(err), type: "error" });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-ui-background min-h-screen w-full overflow-y-auto flex flex-col gap-4 sm:gap-6 items-center justify-center p-4 sm:p-6 md:p-8">
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-texts-dark tracking-wide text-center">
                JANSAHAYAK
            </h1>

            <div className="w-full max-w-sm sm:max-w-md md:max-w-lg flex flex-col gap-4 sm:gap-5 items-center">
                {/* Toggle — hidden during OTP step */}
                {step === "form" && (
                    <div className="flex bg-white rounded-full shadow-sm shadow-black/10 p-1">
                        <button
                            type="button"
                            onClick={() => setIsUser(true)}
                            className={`px-4 sm:px-6 py-1.5 sm:py-2 text-xs sm:text-sm font-semibold transition-all duration-200 cursor-pointer rounded-full ${isUser
                                ? "bg-buttons text-texts-primary shadow-md shadow-buttons/30"
                                : "text-texts-dark/50 hover:text-texts-dark/80"
                                }`}
                        >
                            Sign In
                        </button>
                        <button
                            type="button"
                            onClick={() => setIsUser(false)}
                            className={`px-4 sm:px-6 py-1.5 sm:py-2 text-xs sm:text-sm font-semibold transition-all duration-200 cursor-pointer rounded-full ${!isUser
                                ? "bg-buttons text-texts-primary shadow-md shadow-buttons/30"
                                : "text-texts-dark/50 hover:text-texts-dark/80"
                                }`}
                        >
                            Sign Up
                        </button>
                    </div>
                )}

                {/* Forms */}
                {step === "form" && isUser && (
                    <SignInForm onSubmit={handleAuthSubmit} loading={loading} />
                )}
                {step === "form" && !isUser && (
                    <SignUpForm onSubmit={handleAuthSubmit} loading={loading} />
                )}
                {step === "otp" && (
                    <OtpForm email={email} onSubmit={handleOtpSubmit} loading={loading} />
                )}
            </div>
        </div>
    );
};

export default Authentication;