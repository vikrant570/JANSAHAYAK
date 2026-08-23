import { NextFunction, Request, Response } from "express";
import jwt from "jsonwebtoken";
import { generateRefreshToken, regenerateAccessToken } from "../utils/renewTokens.js";
import { AccessCookieData } from "../types/index.js";
import Tokens from "../models/auth/tokensModel.js";

interface decodedToken {
  exp: number,
  userID: string
}

export const checkRefreshTokenAuthenticity = async (token: string): Promise<{ valid: boolean, newRequired: boolean, userID: string }> => {
  try {
    const decoded = jwt.verify(token, `${process.env.JWT_SECRET}`) as decodedToken;
    if (!decoded) throw new Error("Failed");

    const tokenAlreadyExists = await Tokens.findOne({
      token: token,
      userID: decoded.userID
    });

    if (!tokenAlreadyExists) throw new Error("Session Expired! Please Login Again.");

    const currentTime = Math.floor(Date.now() / 1000);
    const tokenAge = decoded.exp;

    const timeLeft = tokenAge - currentTime;
    const shouldRegenerate = timeLeft <= 60 * 60 * 24 * 2;

    return { valid: true, newRequired: shouldRegenerate, userID: decoded.userID };
  }
  catch (err) {
    return { valid: false, newRequired: false, userID: "" };
  }
}

const isLoggedIn = async (req: Request, res: Response, next: NextFunction) => {
  const accessToken = req.cookies.access;
  const refreshToken = req.cookies.refresh;
  const secret = process.env.JWT_SECRET;

  const isProduction = process.env.NODE_ENV === "production";
  if (!secret) throw new Error("Unauthorised! Access Revoked.")

  if (!refreshToken) {
    return res.status(401).json({
      success: false,
      message: "User Logged Out, Please Login Again!"
    })
  }

  try {
    if (accessToken) {
      const decoded = jwt.verify(accessToken, secret) as AccessCookieData;
      req.user = decoded;
      return next()
    }

    // Flow Continued -> If access token is not found
    const isAuthentic = await checkRefreshTokenAuthenticity(refreshToken);
    if (!isAuthentic.valid) {
      return res.status(401).json({
        success: false,
        message: "Session Expired! Login Again."
      })
    }

    // Refresh Token Authenticity verified, generate new if neeeded
    const newAccessToken = await regenerateAccessToken(String(isAuthentic.userID));

    if (isAuthentic.newRequired && isAuthentic.userID) {
      // Refresh Token About To Expire -> Renewal needed
      res.clearCookie("refresh");

      const renewedRefreshToken = generateRefreshToken(isAuthentic.userID);
      if (!renewedRefreshToken) throw new Error("Internal Server Error!");

      await Tokens.findOneAndUpdate({ token: refreshToken, userID: isAuthentic.userID }, { $set: { token: renewedRefreshToken } });

      res.cookie("refresh", renewedRefreshToken, {
        httpOnly: true,
        sameSite: isProduction ? "none" : "lax",
        secure: isProduction,
        maxAge: 1000 * 60 * 60 * 24 * 30
      });
    };

    res.cookie("access", newAccessToken, {
      httpOnly: true,
      sameSite: isProduction ? "none" : "lax",
      secure: isProduction,
      maxAge: 1000 * 60 * 60 * 24
    });

    req.user = { userID: isAuthentic.userID };
    return next()

  } catch (error: any) {
    return res.status(500).json({ success: false, error: error.message || "Authentication failed! Please Login Again." });
  }
};

export default isLoggedIn;
