const express = require("express");
const router = express.Router();
const {
    getUserNotifications,
    markAsRead,
    markAllAsRead,
    deleteNotification,
    getUnreadCount,
    generateJourneyReminders
} = require("../controllers/Notifications");

// Get all notifications for the authenticated user
router.get("/user", getUserNotifications);

// Get unread notification count
router.get("/unread-count", getUnreadCount);

// Mark a specific notification as read
router.put("/:id/read", markAsRead);

// Mark all notifications as read
router.put("/mark-all-read", markAllAsRead);

// Delete a notification
router.delete("/:id", deleteNotification);

// Demo route to generate journey reminders (for testing)
router.post("/demo/generate-reminders", async (req, res) => {
    try {
        await generateJourneyReminders();
        res.status(200).json({ message: "Journey reminders generated successfully" });
    } catch (error) {
        res.status(500).json({ error: "Failed to generate journey reminders" });
    }
});

module.exports = router;
