// inventory-service/src/middleware/auth.js
const jwt = require('jsonwebtoken');
require('dotenv').config();  // Load environment variables from .env file


const authenticateJWT = (req, res, next) => {
  const token = req.headers['authorization']?.split(' ')[1]; // Get token from Authorization header

  if (!token) {
    return res.sendStatus(403); // Forbidden if no token
  }

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => { // Use JWT secret from environment
    if (err) {
      return res.sendStatus(403); // Forbidden if token is invalid
    }
    req.user = user; // Attach user info to request
    next(); // Proceed to the next middleware or route handler
  });
};

module.exports = authenticateJWT;
