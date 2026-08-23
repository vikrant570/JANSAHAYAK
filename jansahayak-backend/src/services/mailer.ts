import OTP from "../models/auth/otpsModel.js";
import otpGen from "otp-generator";
import nodemailer from "nodemailer";

// FUNCTION TO SEND OTPs
export const sendOtp = async (email: string, action: "login" | "register") => {
  const transport = nodemailer.createTransport({
    host: "smtp.gmail.com",
    port: 587,
    secure: false,
    auth: {
      user: process.env.SMTP_EMAIL,
      pass: process.env.SMTP_PASS,
    },
  });

  // Generate OTP to send
  const otp = otpGen.generate(6, {
    upperCaseAlphabets: false,
    lowerCaseAlphabets: false,
    specialChars: false,
  });

  // Save the otp in DB
  try {
    const sentOTP = await OTP.create({
      user: email,
      otp: Number(otp),
    });
  } catch (err: any) {
    if (err.code === 11000) {
      return { success: false, code: 11000 };
    }
  }

  const text = (action == "login" ? "for logging into your account is: " : "for verfiying your email after registration is: ") + otp;
  //Email For Sending OTP
  const mailOptions = {
    from: process.env.SMTP_EMAIL,
    to: email, //recievd at frontend
    subject: "Verification Request.",
    text: "One Time Password " + text
  };

  //Send the mail finally using our transport
  try {
    await transport.sendMail(mailOptions);
    return { success: true, code: 10000 }
  } catch (err) {
    return { success: true, code: 11111 }
  }
};

// Mail after an authentication
export const sendFinalMail = async (
  fullname: string,
  email: string,
  action: string
) => {
  const transport = nodemailer.createTransport({
    host: "smtp.gmail.com",
    port: 587,
    secure: false,
    auth: {
      user: process?.env.SMTP_EMAIL,
      pass: process?.env.SMTP_PASS,
    },
  });

  const text: string =
    action == "register"
      ? `Welcome ${fullname}! \n Thank you for choosing our platform.`
      : `Hey ${fullname}, \nSomeone recently logged in to your account. Report at support@wokhive.com if its not you.`;

  //Email content
  const mailOptions = {
    from: process.env.SMTP_EMAIL,
    to: email, //recievd from frontend
    subject: "Verification Request.",
    text: text,
  };

  //Welcome Mail sent
  transport.sendMail(mailOptions, (err, info) => {
    if (err) {
      return;
    }
  });
};
