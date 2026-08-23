"use client";
import { useState, useRef, useEffect } from "react";
import { LuChevronDown } from "react-icons/lu";
import type { SignUpData } from "@/types/authTypes";

const OCCUPATIONS = ["Student", "Farmer", "Self-employed", "Other"] as const;

const INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
    "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry",
] as const;

/* ── Reusable labeled input ── */
const InputField = ({ label, ...props }: { label: string } & React.InputHTMLAttributes<HTMLInputElement>) => (
    <div className="flex flex-col gap-1 w-full min-w-0">
        <label className="text-texts-dark/60 text-xs sm:text-sm font-bold self-start">{label}</label>
        <input {...props} className={`w-full text-xs sm:text-sm ${props.className ?? ""}`} />
    </div>
);

/* ── Reusable dropdown select ── */
const Dropdown = ({
    label, placeholder, value, options, scrollable, onChange,
}: {
    label: string; placeholder: string; value: string;
    options: readonly string[]; scrollable?: boolean;
    onChange: (val: string) => void;
}) => {
    const [open, setOpen] = useState(false);
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const close = (e: MouseEvent | TouchEvent) => {
            if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
        };
        document.addEventListener("mousedown", close);
        document.addEventListener("touchstart", close);
        return () => {
            document.removeEventListener("mousedown", close);
            document.removeEventListener("touchstart", close);
        };
    }, []);

    return (
        <div className="flex flex-col gap-1 w-full min-w-0" ref={ref}>
            <label className="text-texts-dark/60 text-xs sm:text-sm font-bold self-start">{label}</label>
            <div className="relative w-full">
                <button
                    type="button"
                    onClick={() => setOpen(!open)}
                    className={`w-full text-left border-[1.5px] border-ui-tertiary rounded-[20px] px-3.5 py-2 text-xs sm:text-sm shadow-sm shadow-black/20 flex items-center justify-between cursor-pointer transition-colors duration-150 ${
                        value ? "text-texts-dark" : "text-texts-dark/30"
                    }`}
                >
                    <span className="truncate">{value || placeholder}</span>
                    <LuChevronDown className={`transition-transform duration-200 shrink-0 ml-1 ${open ? "rotate-180" : ""}`} />
                </button>

                {open && (
                    <div className={`absolute top-full left-0 mt-1 w-full bg-ui-background shadow-xl shadow-black/20 rounded-xl z-50 overflow-hidden ${
                        scrollable ? "max-h-48 overflow-y-auto" : ""
                    }`}>
                        {options.map((opt, i) => (
                            <button
                                key={opt}
                                type="button"
                                onClick={() => { onChange(opt); setOpen(false); }}
                                className={`w-full text-left hover:bg-ui-tertiary/70 transition-colors duration-150 py-2 sm:py-2.5 px-3.5 text-xs sm:text-sm text-texts-dark/75 cursor-pointer ${
                                    i === 0 ? "rounded-t-xl" : ""
                                } ${i === options.length - 1 ? "rounded-b-xl" : ""} ${
                                    value === opt ? "bg-buttons/15 text-texts-dark font-medium" : ""
                                }`}
                            >
                                {opt}
                            </button>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

/* ── SignUp Form ── */
interface SignUpFormProps {
    onSubmit: (data: SignUpData) => void;
    loading: boolean;
}

const SignUpForm = ({ onSubmit, loading }: SignUpFormProps) => {
    const [form, setForm] = useState({
        email: "", firstName: "", lastName: "",
        password: "", age: "", income: "",
        occupation: "", state: "",
    });

    const set = (key: keyof typeof form) => (val: string) =>
        setForm((prev) => ({ ...prev, [key]: val }));

    const onInput = (key: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) =>
        set(key)(e.target.value);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const { email, firstName, lastName, password, age, income, occupation, state } = form;
        if (!email || !firstName || !lastName || !password || !age || !income || !occupation || !state) return;

        onSubmit({
            name: { first: firstName, last: lastName },
            email,
            password,
            otherDetails: {
                occupation,
                age: Number(age),
                income: Number(income),
                state,
            },
        });
    };

    return (
        <form
            id="auth-form"
            onSubmit={handleSubmit}
            className="flex flex-col gap-3.5 sm:gap-4 items-center justify-center w-full bg-white shadow-black/20 rounded-3xl p-5 sm:p-6 md:p-8 shadow-xl"
        >
            <InputField label="Email Address" type="email" placeholder="youremail@example.com"
                value={form.email} onChange={onInput("email")} required />

            <div className="flex flex-col md:flex-row w-full gap-3 sm:gap-4">
                <InputField label="First Name" type="text" placeholder="First Name"
                    value={form.firstName} onChange={onInput("firstName")} required />
                <InputField label="Last Name" type="text" placeholder="Last Name"
                    value={form.lastName} onChange={onInput("lastName")} required />
            </div>

            <InputField label="Password" type="password" placeholder="Create a password"
                value={form.password} onChange={onInput("password")} required />

            <div className="flex flex-col md:flex-row w-full gap-3 sm:gap-4">
                <InputField label="Age" type="number" placeholder="e.g. 25"
                    value={form.age} onChange={onInput("age")} required min={1} max={120} />
                <InputField label="Annual Income (₹)" type="number" placeholder="e.g. 500000"
                    value={form.income} onChange={onInput("income")} required min={0} />
            </div>

            <div className="flex flex-col md:flex-row w-full gap-3 sm:gap-4">
                <Dropdown label="Occupation" placeholder="Select Occupation"
                    value={form.occupation} options={OCCUPATIONS} onChange={set("occupation")} />
                <Dropdown label="State" placeholder="Select State" scrollable
                    value={form.state} options={INDIAN_STATES} onChange={set("state")} />
            </div>

            <button
                type="submit"
                disabled={loading}
                className="bg-buttons text-texts-primary cursor-pointer font-semibold shadow-buttons/20 shadow-md hover:shadow-lg hover:shadow-buttons/40 transition-all duration-100 px-6 sm:px-8 py-2 sm:py-2.5 text-xs sm:text-sm md:text-base rounded-full mt-1 sm:mt-2 disabled:opacity-50"
            >
                {loading ? "Signing Up..." : "Sign Up"}
            </button>
        </form>
    );
};

export default SignUpForm;
