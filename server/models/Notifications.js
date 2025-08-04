module.exports = (sequelize, DataTypes) => {
    const Notifications = sequelize.define("Notifications", {
        type: {
            type: DataTypes.ENUM('booking_created', 'booking_confirmed', 'booking_cancelled', 'journey_reminder', 'journey_started', 'journey_completed', 'system_alert'),
            allowNull: false,
            defaultValue: 'system_alert'
        },
        title: {
            type: DataTypes.STRING,
            allowNull: false
        },
        message: {
            type: DataTypes.TEXT,
            allowNull: false
        },
        isRead: {
            type: DataTypes.BOOLEAN,
            allowNull: false,
            defaultValue: false
        },
        bookingId: {
            type: DataTypes.INTEGER,
            allowNull: true,
            references: {
                model: 'Bookings',
                key: 'id'
            }
        },
        scheduledFor: {
            type: DataTypes.DATE,
            allowNull: true
        },
        priority: {
            type: DataTypes.ENUM('low', 'medium', 'high', 'urgent'),
            allowNull: false,
            defaultValue: 'medium'
        },
        actionUrl: {
            type: DataTypes.STRING,
            allowNull: true
        },
        metadata: {
            type: DataTypes.JSON,
            allowNull: true
        }
    });

    Notifications.associate = (models) => {
        Notifications.belongsTo(models.User, { foreignKey: "userId" });
        Notifications.belongsTo(models.Bookings, { foreignKey: "bookingId" });
    };

    return Notifications;
};
