const bcrypt = require("bcryptjs")
const jwt = require("jsonwebtoken")
const {User} = require("../models")



const register = async(req,res)=>{
    try {


        const { firstName, initialNames, lastName, email,password}= req.body
        if (!firstName || !lastName || !email || !password){
            return res.status(400).json({error:"All fields are required!!"})
        }
        const userExist = await User.findOne({where:{email}})
        if(userExist){
            return res.status(400).json({error:"User with same email found"})
        }
        const hashPassword = await bcrypt.hash(password, 10)
        if(hashPassword){
            const createUser = await User.create({firstName, initialNames,lastName, email, password:hashPassword})
            if(createUser){
                return res.status(201).json({message:"User created"})
            }
        }
        
    } catch (error) {
        console.log(error)
        process.exit(1)
    }
}


const login = async(req,res)=>{
    try {

        const { email , password} = req.body
        if(!email || !password){
            return res.status(400).json({error:"All fields are required"})
        }
        

        const searchUser = await User.findOne({where:{email}})
        if(searchUser){
            const passwordMatch = await bcrypt.compare(password, searchUser.password)
            if(!passwordMatch){
                return res.status(400).json({error:"Incorrect password"})
            }
            // Only include the fields you want in the JWT payload
            const token = jwt.sign({
                firstName: searchUser.firstName,
                lastName: searchUser.lastName,
                initialNames: searchUser.initialNames,
                profilePicture: searchUser.profilePicture,
                email: searchUser.email
            }, "secret here", {expiresIn : "20m"})
            if(token){
                return res.status(200).json({firstName:searchUser.firstName, lastName:searchUser.lastName, initialNames: searchUser.initialNames, token:token})
            }
        }else{
            return res.status(404).json({error:"user not found"})
        }
    } catch (error) {
        console.log(error)
        process.exit(1)
    }
}


module.exports = { register,login }