const express = require("express")
const { register, login, updateProfilePicture } = require("../controllers/Users")


const router = express.Router()


router.post("/register", register)
router.post("/login", login)
router.put("/profile-picture", updateProfilePicture)




module.exports = router