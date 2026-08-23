import api from "./axiosInstance";
import type { SignInData, SignUpData, OtpData, AuthAction } from "@/types/authTypes";

const AUTH_ENDPOINTS: Record<AuthAction, string> = {
    login: "/auth/login",
    register: "/auth/register",
};

export async function submitAuth(data: SignInData | SignUpData, action: AuthAction) {
    const response = await api.post(AUTH_ENDPOINTS[action], data);
    return response;
}

export async function verifyOtp(data: OtpData, action: AuthAction) {
    const response = await api.post("/auth/verifyOtp", { ...data, action: action });
    return response;
}
