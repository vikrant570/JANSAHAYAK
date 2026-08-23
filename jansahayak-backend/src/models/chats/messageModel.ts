import mongoose, { Schema } from "mongoose";

const messageSchema = new Schema({
    chatID: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'chats',
        required: true
    },
    content: {
        type: String,
        required: true
    },
    role: {
        type: String,
        enum: ["assistant", "user"],
        required: true
    }
}, { timestamps: true })

export const Message = mongoose.model("messages", messageSchema)