

module.exports = (sequelize, DataTypes)=>{

    const User = sequelize.define("User", {
        firstName:{
            type:DataTypes.STRING,
            allowNull:false
        },
        initialNames:{
            type:DataTypes.STRING,
            allowNull:true
        },
        lastName:{
            type:DataTypes.STRING,
            allowNull:false
        },
        email:{
            type:DataTypes.STRING,
            allowNull:false,
            unique:true
        },
        password:{
            type:DataTypes.STRING,
            allowNull:true,
        },
        profilePicture:{
             type:DataTypes.STRING,
            allowNull:false,
            defaultValue:"https://static.vecteezy.com/system/resources/thumbnails/020/765/399/small_2x/default-profile-account-unknown-icon-black-silhouette-free-vector.jpg"
        }
    })

    User.associate = (models)=>{
        User.hasMany(models.Bookings, {foreignKey:"userId"})
    }

    return User

}