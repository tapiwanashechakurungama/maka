const express = require("express")
const cors = require("cors")
const db = require("./models")
const userRoutes = require("./routes/Users")
const bookingRoutes = require("./routes/Bookings")
const notificationRoutes = require("./routes/Notifications")

const app = express()

app.use(express.json())
app.use(express.urlencoded({extended:false}))
app.use(cors())
app.use("/users",userRoutes)
app.use("/bookings",bookingRoutes)
app.use("/notifications",notificationRoutes)

db.sequelize.sync().then(()=>{
    app.listen(8080,()=>{
        console.log("server up")
    })
}).catch(error =>{
    console.log(error.message)
    process.exit(1)
})