import express, { NextFunction, Request, Response } from "express";
import cors from "cors";
import chatsGateway from "./routes/chatsGateway.js";
import userGateway from "./routes/userGateway.js";
import profiles from "./routes/profiles.js";
import mongoose from "mongoose";
import cookieParser from "cookie-parser";
import isLoggedIn from "./middlewares/isLoggedIn.js";
import agentGateway from "./routes/agentGateway.js";

const app = express();
app.use(cookieParser());
app.use(cors({
  origin: [process.env.CLIENT_URL],
  credentials: true
}));
app.use(express.json());
app.use("/chats", isLoggedIn, chatsGateway)
app.use("/auth", userGateway)
app.use("/profiles", isLoggedIn, profiles)
app.use("/agent", agentGateway)


const { PORT } = process.env;

app.listen(PORT, async () => {
  const { DB_URL } = process.env;
  const isDevelopment = process.env.NODE_ENV === "development"
  if (!DB_URL) throw new Error("Please provide DB_URL");

  await mongoose.connect(String(DB_URL)).then(() =>
    isDevelopment && console.log("Database connected")
  ).catch((err) => {
    console.log(err)
  })
  console.log("Backend running on http://localhost:5000");
});

//Global Error handler
interface Error {
  status: number,
  message: string
}
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  let errorMessage = err.message;

  res.status(err.status || 500).json({
    success: false,
    message: errorMessage || "Something Went Wrong !"
  })
})