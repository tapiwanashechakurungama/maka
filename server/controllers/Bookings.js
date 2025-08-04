const db = require("../models");
const Bookings = db.Bookings;
const User = db.User;
const jwt = require("jsonwebtoken");
const { createBookingNotification } = require("./Notifications");

// Create a new booking
const createBooking = async (req, res) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) {
            return res.status(401).json({ error: "Access token required" });
        }

        const decoded = jwt.verify(token, "your-secret-key");
        const userId = decoded.id;

        const { from, to, date, time, numberOfPassengers, phoneNumber } = req.body;

        // Validate required fields
        if (!from || !to || !date || !time || !phoneNumber) {
            return res.status(400).json({ error: "Missing required fields" });
        }

        // Calculate price based on distance (you can modify this logic)
        const price = calculatePrice(from, to, numberOfPassengers || 1);

        // Generate bus number and driver name (in real app, this would come from available buses)
        const busNumber = generateBusNumber();
        const driverName = generateDriverName();

        const booking = await Bookings.create({
            from,
            to,
            date,
            time,
            numberOfPassengers: numberOfPassengers || 1,
            phoneNumber,
            userId,
            price,
            busNumber,
            driverName,
            status: 'pending'
        });

        // Create notification for booking creation
        await createBookingNotification(booking, 'booking_created');

        res.status(201).json({
            message: "Booking created successfully",
            booking: {
                id: booking.id,
                from: booking.from,
                to: booking.to,
                date: booking.date,
                time: booking.time,
                numberOfPassengers: booking.numberOfPassengers,
                phoneNumber: booking.phoneNumber,
                status: booking.status,
                busNumber: booking.busNumber,
                driverName: booking.driverName,
                price: booking.price
            }
        });
    } catch (error) {
        console.error("Error creating booking:", error);
        res.status(500).json({ error: "Failed to create booking" });
    }
};

// Get all bookings for a user
const getUserBookings = async (req, res) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) {
            return res.status(401).json({ error: "Access token required" });
        }

        const decoded = jwt.verify(token, "your-secret-key");
        const userId = decoded.id;

        const bookings = await Bookings.findAll({
            where: { userId },
            order: [['createdAt', 'DESC']]
        });

        res.status(200).json({
            bookings: bookings.map(booking => ({
                id: booking.id,
                from: booking.from,
                to: booking.to,
                date: booking.date,
                time: booking.time,
                numberOfPassengers: booking.numberOfPassengers,
                phoneNumber: booking.phoneNumber,
                status: booking.status,
                busNumber: booking.busNumber,
                driverName: booking.driverName,
                price: booking.price,
                createdAt: booking.createdAt
            }))
        });
    } catch (error) {
        console.error("Error fetching user bookings:", error);
        res.status(500).json({ error: "Failed to fetch bookings" });
    }
};

// Get a specific booking by ID
const getBookingById = async (req, res) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) {
            return res.status(401).json({ error: "Access token required" });
        }

        const decoded = jwt.verify(token, "your-secret-key");
        const userId = decoded.id;
        const bookingId = req.params.id;

        const booking = await Bookings.findOne({
            where: { id: bookingId, userId }
        });

        if (!booking) {
            return res.status(404).json({ error: "Booking not found" });
        }

        res.status(200).json({
            booking: {
                id: booking.id,
                from: booking.from,
                to: booking.to,
                date: booking.date,
                time: booking.time,
                numberOfPassengers: booking.numberOfPassengers,
                phoneNumber: booking.phoneNumber,
                status: booking.status,
                busNumber: booking.busNumber,
                driverName: booking.driverName,
                price: booking.price,
                createdAt: booking.createdAt
            }
        });
    } catch (error) {
        console.error("Error fetching booking:", error);
        res.status(500).json({ error: "Failed to fetch booking" });
    }
};

// Update booking status (admin function)
const updateBookingStatus = async (req, res) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) {
            return res.status(401).json({ error: "Access token required" });
        }

        const decoded = jwt.verify(token, "your-secret-key");
        const userId = decoded.id;
        const bookingId = req.params.id;
        const { status } = req.body;

        if (!status || !['pending', 'confirmed', 'completed', 'cancelled'].includes(status)) {
            return res.status(400).json({ error: "Invalid status" });
        }

        const booking = await Bookings.findOne({
            where: { id: bookingId, userId }
        });

        if (!booking) {
            return res.status(404).json({ error: "Booking not found" });
        }

        // Additional validation for status transitions
        if (booking.status === 'cancelled' && status !== 'cancelled') {
            return res.status(400).json({ error: "Cannot update cancelled booking" });
        }

        if (booking.status === 'completed' && status !== 'completed') {
            return res.status(400).json({ error: "Cannot update completed booking" });
        }

        await booking.update({ status });

        // Create notification for status change
        if (status === 'confirmed') {
            await createBookingNotification(booking, 'booking_confirmed');
        }

        res.status(200).json({
            message: "Booking status updated successfully",
            booking: {
                id: booking.id,
                status: booking.status,
                busNumber: booking.busNumber,
                driverName: booking.driverName
            }
        });
    } catch (error) {
        console.error("Error updating booking status:", error);
        res.status(500).json({ error: "Failed to update booking status" });
    }
};

// Cancel a booking
const cancelBooking = async (req, res) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) {
            return res.status(401).json({ error: "Access token required" });
        }

        const decoded = jwt.verify(token, "your-secret-key");
        const userId = decoded.id;
        const bookingId = req.params.id;

        const booking = await Bookings.findOne({
            where: { id: bookingId, userId }
        });

        if (!booking) {
            return res.status(404).json({ error: "Booking not found" });
        }

        if (booking.status === 'cancelled') {
            return res.status(400).json({ error: "Booking is already cancelled" });
        }

        if (booking.status === 'completed') {
            return res.status(400).json({ error: "Cannot cancel completed booking" });
        }

        await booking.update({ status: 'cancelled' });

        // Create notification for booking cancellation
        await createBookingNotification(booking, 'booking_cancelled');

        res.status(200).json({
            message: "Booking cancelled successfully",
            booking: {
                id: booking.id,
                status: booking.status
            }
        });
    } catch (error) {
        console.error("Error cancelling booking:", error);
        res.status(500).json({ error: "Failed to cancel booking" });
    }
};

// Delete a booking (admin only or for pending bookings)
const deleteBooking = async (req, res) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) {
            return res.status(401).json({ error: "Access token required" });
        }

        const decoded = jwt.verify(token, "your-secret-key");
        const userId = decoded.id;
        const bookingId = req.params.id;

        const booking = await Bookings.findOne({
            where: { id: bookingId, userId }
        });

        if (!booking) {
            return res.status(404).json({ error: "Booking not found" });
        }

        // Only allow deletion of pending or cancelled bookings
        if (booking.status !== 'pending' && booking.status !== 'cancelled') {
            return res.status(400).json({ error: "Cannot delete confirmed or completed booking" });
        }

        await booking.destroy();

        res.status(200).json({
            message: "Booking deleted successfully"
        });
    } catch (error) {
        console.error("Error deleting booking:", error);
        res.status(500).json({ error: "Failed to delete booking" });
    }
};

// Demo function to auto-confirm some bookings (for testing)
const autoConfirmBookings = async () => {
    try {
        const pendingBookings = await Bookings.findAll({
            where: { status: 'pending' },
            limit: 2 // Only confirm 2 bookings at a time
        });

        for (const booking of pendingBookings) {
            await booking.update({ 
                status: 'confirmed',
                busNumber: generateBusNumber(),
                driverName: generateDriverName()
            });
        }

        console.log(`Auto-confirmed ${pendingBookings.length} bookings`);
    } catch (error) {
        console.error('Error auto-confirming bookings:', error);
    }
};

// Helper functions
const calculatePrice = (from, to, passengers) => {
    // Simple price calculation - you can make this more sophisticated
    const basePrice = 3.50;
    const passengerMultiplier = passengers * 0.5;
    return parseFloat((basePrice + passengerMultiplier).toFixed(2));
};

const generateBusNumber = () => {
    const busNumbers = ['BUS-001', 'BUS-002', 'BUS-003', 'BUS-004', 'BUS-005'];
    return busNumbers[Math.floor(Math.random() * busNumbers.length)];
};

const generateDriverName = () => {
    const drivers = ['John Smith', 'Sarah Johnson', 'Mike Wilson', 'Lisa Brown', 'David Lee'];
    return drivers[Math.floor(Math.random() * drivers.length)];
};

module.exports = {
    createBooking,
    getUserBookings,
    getBookingById,
    updateBookingStatus,
    cancelBooking,
    deleteBooking,
    autoConfirmBookings
};
