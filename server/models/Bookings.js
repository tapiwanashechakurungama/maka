

module.exports = (sequelize, DataTypes)=>{

    const Bookings = sequelize.define("Bookings", {
        from:{
            type:DataTypes.STRING,
            allowNull:false
        },
        to:{
            type:DataTypes.STRING,
            allowNull:false
        },
        date:{
            type:DataTypes.STRING,
            allowNull:false
        },
        time:{
            type:DataTypes.STRING,
            allowNull:false,
        },
        numberOfPassengers:{
            type:DataTypes.INTEGER,
            allowNull:true,
        },
        phoneNumber:{
             type:DataTypes.STRING,
            allowNull:false,
        },
        status: {
            type: DataTypes.ENUM('pending', 'confirmed', 'completed', 'cancelled'),
            allowNull: false,
            defaultValue: 'pending'
        },
        busNumber: {
            type: DataTypes.STRING,
            allowNull: true,
        },
        driverName: {
            type: DataTypes.STRING,
            allowNull: true,
        },
        price: {
            type: DataTypes.DECIMAL(10, 2),
            allowNull: true,
        }
    })

    Bookings.associate = (models)=>{
        Bookings.belongsTo(models.User, {foreignKey:"userId"})
    }

    return Bookings

}