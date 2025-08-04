const express = require("express");
const router = express.Router();
const {
    createBooking,
    getUserBookings,
    getBookingById,
    updateBookingStatus,
    cancelBooking,
    deleteBooking
} = require("../controllers/Bookings");

// Import the auto-confirm function
const { autoConfirmBookings } = require("../controllers/Bookings");

// Create a new booking
router.post("/create", createBooking);

// Get all bookings for the authenticated user
router.get("/user", getUserBookings);

// Get a specific booking by ID
router.get("/:id", getBookingById);

// Update booking status
router.put("/:id/status", updateBookingStatus);

// Cancel a booking
router.put("/:id/cancel", cancelBooking);

// Delete a booking
router.delete("/:id", deleteBooking);

// Demo route to auto-confirm pending bookings (for testing)
router.post("/demo/auto-confirm", async (req, res) => {
    try {
        await autoConfirmBookings();
        res.status(200).json({ message: "Auto-confirmation completed" });
    } catch (error) {
        res.status(500).json({ error: "Failed to auto-confirm bookings" });
    }
});

module.exports = router;
