// auth-service/src/routes/auth.js
const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../models/user');
require('dotenv').config();  // Load environment variables from .env file

const router = express.Router();

router.post('/register', async (req, res) => {
  try {
    const { username, password } = req.body;
    const userId = await User.createUser(username, password);
    res.status(201).json({ message: 'User registered successfully', userId });
  } catch (error) {
    res.status(500).json({ error: 'Error registering user' });
  }
});

router.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    const user = await User.findByUsername(username);
    
    if (user && await bcrypt.compare(password, user.password)) {
      const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' }); // Use JWT secret from environment
      res.json({ token });
    } else {
      res.status(401).json({ error: 'Invalid credentials' });
    }
  } catch (error) {
    console.error('Login error:', error); // Log the error for debugging
    res.status(500).json({ error: 'Error logging in' });
  }
});

router.post('/verify', (req, res) => {
  const token = req.body.token;
  if (!token) return res.status(400).json({ error: 'Token is required' });

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET); // Use JWT secret from environment
    res.json({ valid: true, userId: decoded.userId });
  } catch (error) {
    res.json({ valid: false });
  }
});

module.exports = { authRouter: router };


