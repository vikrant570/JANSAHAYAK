import { Response, Request } from 'express';
import Tokens from "../models/auth/tokensModel.js";
import jwt from 'jsonwebtoken';
import { checkRefreshTokenAuthenticity } from '../middlewares/isLoggedIn.js';
import { generateRefreshToken } from './renewTokens.js';


// For Login and Register ---
const assignCookiesOnAuth = async (res: Response, userID: string) => {
  const secret = process.env.JWT_SECRET;
  if (!secret) throw new Error("Unauthorised Access!");
  const isProduction = process.env.NODE_ENV === "production";

  // getting refreshToken, whether we require new or old
  const getRefreshToken = async (): Promise<string> => {
    const tokenAlreadyExists = await Tokens.findOne({ userID: userID }, { token: 1 });
    const prevTokn = tokenAlreadyExists?.token;

    if (prevTokn) {
      const isAuthentic = await checkRefreshTokenAuthenticity(prevTokn);
      if (isAuthentic.valid && !isAuthentic.newRequired) {
        return prevTokn;
      }
      else {
        const newRefreshToken = generateRefreshToken(userID);
        tokenAlreadyExists.token = newRefreshToken;
        await tokenAlreadyExists.save();
        return newRefreshToken;
      }
    }

    const newRefreshToken = generateRefreshToken(userID);
    await Tokens.create({ userID: userID, token: newRefreshToken });
    return newRefreshToken;
  }

  const refreshToken = await getRefreshToken();
  const accessToken = jwt.sign({ userID: userID }, secret, { expiresIn: "24h" });


  res.cookie("access", accessToken, {
    httpOnly: true,
    sameSite: isProduction ? "none" : "lax",
    secure: isProduction,
    maxAge: 1000 * 60 * 60 * 24
  });

  res.cookie("refresh", refreshToken, {
    httpOnly: true,
    sameSite: isProduction ? "none" : "lax",
    secure: isProduction,
    maxAge: 1000 * 60 * 60 * 24 * 30
  })
};

export default assignCookiesOnAuth;