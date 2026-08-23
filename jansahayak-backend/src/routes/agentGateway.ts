import express from "express";
import routeHandler from "../middlewares/globalErrWrap.js";
import Users from "../models/auth/usersModel.js";
import jwt from "jsonwebtoken";
import { Chat } from "../models/chats/chatsModel.js";
import { Message } from "../models/chats/messageModel.js";
import { Types } from "mongoose";
const router = express.Router();

router.post("/chat", routeHandler(async (req, res) => {
    const { prompt, chatID } = req.body;
    if (!prompt) throw Object.assign(new Error("Prompt is required!"), { status: 400 });


    const token = req.cookies.refresh;
    const { userID } = token && jwt.verify(token, process.env.JWT_SECRET) as { userID: string }
    const profile = (token && userID && await Users.findById(userID).select("otherDetails").lean().exec()) || null;

    const chat = async () => {
        if (chatID && profile._id) {
            // If user is logged in chatID can't be empty, prior chat creation functions are there.
            const currentChat = await Chat.findById(chatID);
            await Message.create({
                chatID: currentChat?._id,
                role: "user",
                content: prompt,
            })
            return currentChat;
        }
        else {
            return null;
        }
    };
    const foundChat = await chat();

    if (userID && foundChat && String(foundChat.user) != userID) {
        throw Object.assign(new Error("Unauthorised Access! Not your chat."), { status: 403 })
    }

    const top_k = prompt.length > 40 ? 6 : (prompt.length > 25 ? 5 : 3)

    const response = await fetch(`${process.env.AI_API_BASE_URL}/api/v1/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: prompt, profile: profile || null, top_k })
    });

    const data = await response.json() as { status: boolean; answer: string; };
    if (!data || !data.status) throw Object.assign(new Error("Connection Refused! Try again later..."), { status: 500 });

    if (chatID && profile && foundChat) {
        await Message.create({
            chatID: new Types.ObjectId(chatID),
            role: "assistant",
            content: String(data.answer)
        })
    }
    return res.status(200).json(data);
}))

export default router;