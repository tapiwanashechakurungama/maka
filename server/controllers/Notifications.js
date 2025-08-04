const db = require("../models");
const Notifications = db.Notifications;
const User = db.User;
const Bookings = db.Bookings;
const jwt = require("jsonwebtoken");

// Get all notifications for a user
const getUserNotifications = async (req, res) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) {
            return res.status(401).json({ error: "Access token required" });
        }

        const decoded = jwt.verify(token, "your-secret-key");
        const userId = decoded.id;

        const notifications = await Notifications.findAll({
            where: { userId },
            include: [
                {
                    model: Bookings,
                    attributes: ['id', 'from', 'to', 'date', 'time', 'status']
                }
            ],
            order: [['createdAt', 'DESC']]
        });

        res.status(200).json({
            notifications: notifications.map(notification => ({
                id: notification.id,
                type: notification.type,
                title: notification.title,
                message: notification.message,
                isRead: notification.isRead,
                priority: notification.priority,
                scheduledFor: notification.scheduledFor,
                actionUrl: notification.actionUrl,
                metadata: notification.metadata,
                booking: notification.Booking,
                createdAt: notification.createdAt
            }))
        });
    } catch (error) {
        console.error("Error fetching notifications:", error);
        res.status(500).json({ error: "Failed to fetch notifications" });
    }
};

// Mark notification as read
const markAsRead = async (req, res) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) {
            return res.status(401).json({ error: "Access token required" });
        }

        const decoded = jwt.verify(token, "your-secret-key");
        const userId = decoded.id;
        const notificationId = req.params.id;

        const notification = await Notifications.findOne({
            where: { id: notificationId, userId }
        });

        if (!notification) {
            return res.status(404).json({ error: "Notification not found" });
        }

        await notification.update({ isRead: true });

        res.status(200).json({
            message: "Notification marked as read",
            notification: {
                id: notification.id,
                isRead: notification.isRead
            }
        });
    } catch (error) {
        console.error("Error marking notification as read:", error);
        res.status(500).json({ error: "Failed to mark notification as read" });
    }
};

// Mark all notifications as read
const markAllAsRead = async (req, res) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) {
            return res.status(401).json({ error: "Access token required" });
        }

        const decoded = jwt.verify(token, "your-secret-key");
        const userId = decoded.id;

        await Notifications.update(
            { isRead: true },
            { where: { userId, isRead: false } }
        );

        res.status(200).json({
            message: "All notifications marked as read"
        });
    } catch (error) {
        console.error("Error marking all notifications as read:", error);
        res.status(500).json({ error: "Failed to mark notifications as read" });
    }
};

// Delete a notification
const deleteNotification = async (req, res) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) {
            return res.status(401).json({ error: "Access token required" });
        }

        const decoded = jwt.verify(token, "your-secret-key");
        const userId = decoded.id;
        const notificationId = req.params.id;

        const notification = await Notifications.findOne({
            where: { id: notificationId, userId }
        });

        if (!notification) {
            return res.status(404).json({ error: "Notification not found" });
        }

        await notification.destroy();

        res.status(200).json({
            message: "Notification deleted successfully"
        });
    } catch (error) {
        console.error("Error deleting notification:", error);
        res.status(500).json({ error: "Failed to delete notification" });
    }
};

// Get unread notification count
const getUnreadCount = async (req, res) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) {
            return res.status(401).json({ error: "Access token required" });
        }

        const decoded = jwt.verify(token, "your-secret-key");
        const userId = decoded.id;

        const count = await Notifications.count({
            where: { userId, isRead: false }
        });

        res.status(200).json({
            unreadCount: count
        });
    } catch (error) {
        console.error("Error getting unread count:", error);
        res.status(500).json({ error: "Failed to get unread count" });
    }
};

// Create a notification (internal function)
const createNotification = async (userId, type, title, message, bookingId = null, priority = 'medium', scheduledFor = null, metadata = null) => {
    try {
        const notification = await Notifications.create({
            userId,
            type,
            title,
            message,
            bookingId,
            priority,
            scheduledFor,
            metadata
        });
        return notification;
    } catch (error) {
        console.error("Error creating notification:", error);
        return null;
    }
};

// Generate journey reminder notifications
const generateJourneyReminders = async () => {
    try {
        const now = new Date();
        const oneHourFromNow = new Date(now.getTime() + 60 * 60 * 1000); // 1 hour from now
        const thirtyMinutesFromNow = new Date(now.getTime() + 30 * 60 * 1000); // 30 minutes from now

        // Find bookings that are within 1 hour and haven't been reminded yet
        const upcomingBookings = await Bookings.findAll({
            where: {
                status: ['confirmed', 'pending'],
                date: now.toISOString().split('T')[0] // Today's date
            },
            include: [
                {
                    model: User,
                    attributes: ['id', 'firstName', 'lastName']
                }
            ]
        });

        for (const booking of upcomingBookings) {
            const bookingTime = new Date(`${booking.date}T${booking.time}`);
            const timeDiff = bookingTime.getTime() - now.getTime();
            const hoursDiff = timeDiff / (1000 * 60 * 60);

            // Check if we should send a reminder
            if (hoursDiff <= 1 && hoursDiff > 0) {
                // Check if reminder already exists
                const existingReminder = await Notifications.findOne({
                    where: {
                        userId: booking.userId,
                        bookingId: booking.id,
                        type: 'journey_reminder'
                    }
                });

                if (!existingReminder) {
                    const priority = hoursDiff <= 0.5 ? 'urgent' : 'high';
                    const title = hoursDiff <= 0.5 ? '🚌 Your journey starts soon!' : '⏰ Journey Reminder';
                    const message = hoursDiff <= 0.5 
                        ? `Your bus from ${booking.from} to ${booking.to} departs in ${Math.round(hoursDiff * 60)} minutes. Please be ready!`
                        : `Your journey from ${booking.from} to ${booking.to} starts in ${Math.round(hoursDiff * 60)} minutes.`;

                    await createNotification(
                        booking.userId,
                        'journey_reminder',
                        title,
                        message,
                        booking.id,
                        priority,
                        bookingTime
                    );
                }
            }
        }

        console.log('Journey reminders generated successfully');
    } catch (error) {
        console.error('Error generating journey reminders:', error);
    }
};

// Create booking-related notifications
const createBookingNotification = async (booking, type) => {
    try {
        const user = await User.findByPk(booking.userId);
        if (!user) return;

        let title, message, priority;

        switch (type) {
            case 'booking_created':
                title = '✅ Booking Confirmed';
                message = `Your booking from ${booking.from} to ${booking.to} on ${booking.date} at ${booking.time} has been created successfully.`;
                priority = 'medium';
                break;
            case 'booking_confirmed':
                title = '🚌 Bus Assigned!';
                message = `Your booking has been confirmed! Bus ${booking.busNumber} with driver ${booking.driverName} will pick you up from ${booking.from}.`;
                priority = 'high';
                break;
            case 'booking_cancelled':
                title = '❌ Booking Cancelled';
                message = `Your booking from ${booking.from} to ${booking.to} has been cancelled.`;
                priority = 'medium';
                break;
            default:
                return;
        }

        await createNotification(
            booking.userId,
            type,
            title,
            message,
            booking.id,
            priority
        );
    } catch (error) {
        console.error('Error creating booking notification:', error);
    }
};

module.exports = {
    getUserNotifications,
    markAsRead,
    markAllAsRead,
    deleteNotification,
    getUnreadCount,
    createNotification,
    generateJourneyReminders,
    createBookingNotification
};
