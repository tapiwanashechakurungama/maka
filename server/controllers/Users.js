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
                id: searchUser.id,
                firstName: searchUser.firstName,
                lastName: searchUser.lastName,
                initialNames: searchUser.initialNames,
                profilePicture: searchUser.profilePicture,
                email: searchUser.email
            }, "your-secret-key", {expiresIn : "20m"})
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

// Function to update user profile picture
const updateProfilePicture = async (req, res) => {
  try {
    // Verify JWT token
    const token = req.headers.authorization?.split(' ')[1];
    
    if (!token) {
      return res.status(401).json({ error: "Authentication token required" });
    }
    
    let decoded;
    try {
      decoded = jwt.verify(token, "your-secret-key");
    } catch (err) {
      return res.status(401).json({ error: "Invalid token" });
    }
    
    const userId = decoded.id;
    
    const { profilePicture } = req.body;
    
    if (!profilePicture) {
      return res.status(400).json({ error: "Profile picture URL is required" });
    }
    
    // Update user profile picture
    const updatedUser = await User.update(
      { profilePicture },
      { where: { id: userId } }
    );
    
    if (updatedUser[0] === 1) {
      return res.status(200).json({ message: "Profile picture updated successfully" });
    } else {
      return res.status(404).json({ error: "User not found" });
    }
  } catch (error) {
    console.log(error);
    return res.status(500).json({ error: "Internal server error" });
  }
};

module.exports = { register,login,updateProfilePicture }