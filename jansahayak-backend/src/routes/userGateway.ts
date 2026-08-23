import Users from "../models/auth/usersModel.js";
import express from "express";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import { sendOtp, sendFinalMail } from "../services/mailer.js";
import OTP from "../models/auth/otpsModel.js";
import routeHandler from "../middlewares/globalErrWrap.js";
import otpCrossCheck from "../utils/otpCrossCheck.js";
import assignCookiesOnAuth from "../utils/assignNewCookies.js";

const router = express.Router();

router.post("/login", routeHandler(async (req, res) => {
  const isProduction = process.env.NODE_ENV === "production";
  const secret = process.env.JWT_SECRET;

  const { email, password } = req.body;

  const user = await Users.findOne({ email }).lean();
  if (!user)
    throw Object.assign(new Error("User not found!"), { status: 404 });

  const isValid = await bcrypt.compare(password, user.password as string);
  if (!isValid)
    throw Object.assign(new Error("Invalid Password!"), { status: 400 });

  const sentMail: { success: boolean, code: number } = await sendOtp(email, "login");
  if (!sentMail.success) throw Object.assign(new Error("OTP could not be sent. Please try again."), { status: 400 });

  const otpAuthCookie = jwt.sign({ email: email }, secret as string, { expiresIn: "5m" })

  res.cookie("otpAuth", otpAuthCookie, {
    httpOnly: isProduction,
    sameSite: isProduction ? "strict" : "lax",
    secure: isProduction,
    maxAge: 1000 * 60 * 5,
  })

  return res.status(200).json({
    success: true,
    message: "OTP Sent Successfully!",
  });
}))

router.post("/register", routeHandler(async (req, res) => {
  const isProduction = process.env.NODE_ENV === "production";
  const secret = process.env.JWT_SECRET;

  const { email, password, otherDetails, name } = req.body;
  const { state, income, age, occupation } = otherDetails;


  const user = await Users.findOne({ email: email, "name.last": name?.last }).select("_id");
  if (user)
    throw Object.assign(new Error("User already exists!"), { status: 400 });

  const sentMail: { success: boolean, code: number } = await sendOtp(email, "register");
  if (!sentMail.success) throw Object.assign(new Error("OTP could not be sent. Please try again."), { status: 400 });

  const hashedPass = await bcrypt.hash(password, 10);
  const newUser = await Users.create({
    email: email,
    password: String(hashedPass),
    name: {
      first: name.first,
      last: name.last
    },
    otherDetails: {
      age: age ?? 14,
      income: income ?? "",
      occupation: occupation ?? "",
      state: state ?? ""
    }
  });
  if (!newUser) throw Object.assign(new Error("Could not create user!"), { status: 400 });


  const otpAuthCookie = jwt.sign({ email: email }, secret as string, { expiresIn: "5m" });

  res.cookie("otpAuth", otpAuthCookie, {
    httpOnly: isProduction,
    sameSite: isProduction ? "strict" : "lax",
    secure: isProduction,
    maxAge: 1000 * 60 * 5,
  })

  return res.status(200).json({
    success: true,
    message: "OTP Sent Successfully!",
  });
}))

router.post("/verifyOtp", routeHandler(async (req, res) => {
  const { email, otp, action } = req.body;

  const verified = await OTP.findOneAndDelete({ user: email, otp: otp });
  if (!verified) throw Object.assign(new Error("Invalid OTP!"), { status: 400 });

  otpCrossCheck(req, email);
  res.clearCookie("otpAuth");
  const user = action == "register" ? await Users.findOneAndUpdate({ email }, { isVerified: true }).select("name") : await Users.findOne({ email }).select("name");

  if (!user)
    throw Object.assign(new Error("Could not verify credentials!"), { status: 400 })

  await assignCookiesOnAuth(res, String(user._id));
  sendFinalMail(email, "login", [user.name?.first, user.name?.last].join(" "));

  return res.status(200).json({
    success: true,
    message: action == "register" ? "Registration Successfull." : "Logged In Successfully."
  })
}))

router.post("/testing", routeHandler(async (req, res) => {
  return res.status(200).json({ success: true });
}))

export default router;