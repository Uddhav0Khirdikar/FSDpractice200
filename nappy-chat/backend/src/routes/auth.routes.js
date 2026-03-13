import express from "express";
import multer from "multer";
import {
  checkAuth,
  getMe,
  login,
  logout,
  signup,
  updateProfile,
} from "../controllers/auth.controller.js";
import { protectRoute } from "../middleware/auth.middleware.js";

// Configure multer to store file in memory (not on disk)
const upload = multer({ storage: multer.memoryStorage() });

const router = express.Router();

router.post("/signup", signup);

router.post("/login", login);

router.post("/logout", logout);

router.get("/me", protectRoute, getMe);

router.put(
  "/update-profile",
  protectRoute,
  upload.single("profilePic"), // Accept single file
  updateProfile
);

router.get("/check-auth", protectRoute, checkAuth);

export default router;
