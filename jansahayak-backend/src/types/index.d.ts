export interface ChatInterface {
    _id: string;
    title: string;
    user: Types.ObjectId
    model?: string;
    createdAt: string;
    updatedAt: string;
}

export interface AccessCookieData {
    userID: string;
    exp?: number;
}

declare global {
    namespace Express {
        interface Request {
            user?: AccessCookieData
        }
    }
}