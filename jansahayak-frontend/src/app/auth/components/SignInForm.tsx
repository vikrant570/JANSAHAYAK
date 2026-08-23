"use client";
import { useState } from "react";
import type { SignInData } from "@/types/authTypes";

interface SignInFormProps {
    onSubmit: (data: SignInData) => void;
    loading: boolean;
}

const SignInForm = ({ onSubmit, loading }: SignInFormProps) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!email || !password) return;
        onSubmit({ email, password });
    };

    return (
        <form
            id="auth-form"
            onSubmit={handleSubmit}
            className="flex flex-col gap-3.5 sm:gap-4 items-center justify-center w-full bg-white shadow-black/20 rounded-3xl p-5 sm:p-6 md:p-8 shadow-xl"
        >
            <div className="flex flex-col gap-1 w-full">
                <label className="text-texts-dark/60 text-xs sm:text-sm font-bold self-start">Email Address</label>
                <input
                    type="email"
                    placeholder="youremail@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="w-full text-xs sm:text-sm"
                />
            </div>

            <div className="flex flex-col gap-1 w-full">
                <label className="text-texts-dark/60 text-xs sm:text-sm font-bold self-start">Password</label>
                <input
                    type="password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="w-full text-xs sm:text-sm"
                />
            </div>

            <button
                type="submit"
                disabled={loading}
                className="bg-buttons text-texts-primary cursor-pointer font-semibold shadow-buttons/20 shadow-md hover:shadow-lg hover:shadow-buttons/40 transition-all duration-100 px-6 sm:px-8 py-2 sm:py-2.5 text-xs sm:text-sm md:text-base rounded-full mt-1 sm:mt-2 disabled:opacity-50"
            >
                {loading ? "Signing In..." : "Sign In"}
            </button>
        </form>
    );
};

export default SignInForm;
