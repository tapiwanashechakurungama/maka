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

module.exports = router;
