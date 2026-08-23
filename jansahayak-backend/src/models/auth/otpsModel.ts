import mongoose from "mongoose";

const otpSchema = new mongoose.Schema({
    user: {
        type: String,
        index: true,
        unique: true,
        message: "Please Wait Before Trying Again."
    },
    otp: Number,
    createdAt: {
        type: Date,
        default: Date.now,
        expires: 60 * 5 // Document will be automatically deleted after 5 minutes
    }
})

const OTP = mongoose.model('otps', otpSchema);
export default OTP;