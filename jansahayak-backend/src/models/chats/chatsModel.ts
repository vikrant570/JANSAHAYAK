import mongoose from "mongoose";

const chatsSchema = new mongoose.Schema({
    title: {
        type: String,
        maxLength: 40
    },
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "users",
        required: true
    },
    model: {
        type: String
        // to be decided
    }
}, { timestamps: true });

export const Chat = mongoose.model("chats", chatsSchema);