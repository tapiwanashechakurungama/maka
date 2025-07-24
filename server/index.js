const express = require("express")
const cors = require("cors")
const db = require("./models")
const userRoutes = require("./routes/Users")

const app = express()

app.use(express.json())
app.use(express.urlencoded({extended:false}))
app.use(cors())
app.use("/users",userRoutes)

db.sequelize.sync().then(()=>{
    app.listen(8080,()=>{
        console.log("server up")
    })
}).catch(error =>{
    console.log(error.message)
    process.exit(1)
})