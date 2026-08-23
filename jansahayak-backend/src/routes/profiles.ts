import express from "express";
import routeHandler from "../middlewares/globalErrWrap.js";
import Users from "../models/auth/usersModel.js";
const router = express.Router();

router.get("/myDetails", routeHandler(async (req, res) => {
    const userID = req.user?.userID;
    if (!userID) throw Object.assign(new Error("You are not logged in!"), { status: 401 })

    const myProfile = await Users.findById(userID).select("-password -otherDetails");
    res.json({ success: true, profile: myProfile });
}))

export default router;