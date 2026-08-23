import mongoose from "mongoose";

const tokenSchema = new mongoose.Schema({
    userID: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "users",
        required: true
    },
    token: {
        type: String,
        unique: true,
        required: true
    }
})

const Tokens = mongoose.model('tokens', tokenSchema);
export default Tokens;