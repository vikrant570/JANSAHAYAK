export type SignInData = {
    email: string;
    password: string;
};

export type SignUpData = {
    name: { first: string; last: string };
    email: string;
    password: string;
    otherDetails: {
        occupation: string;
        age: number;
        income: number;
        state: string;
    };
};

export type OtpData = {
    otp: number;
    email: string;
};

export type AuthAction = "register" | "login";
