import { Request } from "express";
import jwt from "jsonwebtoken";

const otpCrossCheck = (req: Request, email: string) => {
  //Cross checking OTP verification
  const { otpAuth } = req.cookies;

  if (!otpAuth)
    throw Object.assign(new Error("Please verify OTP first."), {
      status: 401,
    });

  interface decodedToken {
    email: string;
  }
  const info = jwt.verify(otpAuth, `${process.env.JWT_SECRET}`) as decodedToken;

  if (info.email != email)
    throw Object.assign(new Error("Authentication Failed !"), {
      status: 403,
    });
};

export default otpCrossCheck;