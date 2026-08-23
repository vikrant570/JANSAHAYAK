import express from "express";
import routeHandler from "../middlewares/globalErrWrap.js";
import { Message } from "../models/chats/messageModel.js";
import { Chat } from "../models/chats/chatsModel.js";
const router = express.Router();

//Get All Chats
router.get("/", routeHandler(async (req, res) => {
    const userID = req.user?.userID;

    const chats = await Chat.find({ user: userID })
    if (!chats) throw Object.assign(new Error("No chats found"), { statusCode: 404 })

    return res.status(200).json({
        success: true,
        chats: chats
    })
}))

//Create Chat
router.put("/", routeHandler(async (req, res) => {
    const userID = req.user?.userID;
    const { title } = req.body;

    const newChat = await Chat.create({
        user: userID,
        title: title
    })

    return res.status(200).json({
        success: true,
        chat: newChat
    })
}))

router.get("/:chatID", routeHandler(async (req, res) => {
    const { chatID } = req.params;
    const { cursor } = req.query;

    const checkChat = await Chat.findById(chatID).select("_id");
    if (!checkChat) throw Object.assign(new Error("Chat Doesn't Exist!"), { status: 404 })
    const query: any = {
        chatID: chatID,
    };

    // Finding older messages than cursor
    if (cursor && cursor != "") {
        query._id = { $lt: cursor };
    }

    const messages = await Message.find(query)
        .sort({ createdAt: -1 })
        .populate({
            path: "project",
            select: "title",
            strictPopulate: false
        })
        .limit(25)

    const sortedMessages = messages.reverse();

    res.status(200).json({
        success: true,
        messages: sortedMessages,
        hasMore: messages.length === 25
    });
}))

//Delete Chat
router.delete("/:chatId", routeHandler(async (req, res) => {
    const userID = req.user?.userID;
    const { chatId } = req.params;

    const chat = await Chat.deleteOne({ _id: chatId, user: userID })
    if (!chat) throw Object.assign(new Error("Chat not found"), { statusCode: 404 })
    await Message.deleteMany({ chat: chatId })

    return res.status(200).json({
        success: true,
        chat: chat
    })
}))

export default router;