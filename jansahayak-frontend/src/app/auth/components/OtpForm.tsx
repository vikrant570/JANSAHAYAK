"use client";
import { useState } from "react";
import type { OtpData } from "@/types/authTypes";

interface OtpFormProps {
    email: string;
    onSubmit: (data: OtpData) => void;
    loading: boolean;
}

const OtpForm = ({ email, onSubmit, loading }: OtpFormProps) => {
    const [otp, setOtp] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!otp) return;
        onSubmit({ otp: Number(otp), email });
    };

    return (
        <form
            id="auth-form"
            onSubmit={handleSubmit}
            className="flex flex-col gap-3.5 sm:gap-4 items-center justify-center w-full bg-white shadow-black/20 rounded-3xl p-5 sm:p-6 md:p-8 shadow-xl"
        >
            <p className="text-texts-dark/60 text-xs sm:text-sm text-center px-1">
                We sent a verification code to <span className="font-semibold text-texts-dark break-all">{email}</span>
            </p>

            <div className="flex flex-col gap-1 w-full">
                <label className="text-texts-dark/60 text-xs sm:text-sm font-bold self-start">Enter OTP</label>
                <input
                    type="number"
                    placeholder="Enter verification code"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    required
                    className="w-full text-xs sm:text-sm text-center tracking-widest"
                />
            </div>

            <button
                type="submit"
                disabled={loading}
                className="bg-buttons text-texts-primary cursor-pointer font-semibold shadow-buttons/20 shadow-md hover:shadow-lg hover:shadow-buttons/40 transition-all duration-100 px-6 sm:px-8 py-2 sm:py-2.5 text-xs sm:text-sm md:text-base rounded-full mt-1 sm:mt-2 disabled:opacity-50"
            >
                {loading ? "Verifying..." : "Verify"}
            </button>
        </form>
    );
};

export default OtpForm;
