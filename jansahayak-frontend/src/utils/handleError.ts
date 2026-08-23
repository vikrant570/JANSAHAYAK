import axios, { AxiosError } from "axios";
interface Res {
    message: string;
}

export const handleAxiosError = (error: any) => {
    if (axios.isAxiosError(error)) {
        const data = (error as AxiosError).response?.data;

        if (typeof data === "string") return data;
        return (data as Res)?.message || error.message;
    }

    return (error as Error).message || "Something Went Wrong!";
}