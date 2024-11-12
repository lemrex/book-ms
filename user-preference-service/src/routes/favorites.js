// user-preferences-service/src/routes/favorites.js
const express = require('express');
const Favorite = require('../models/favorite');
const { getChannel } = require('../config/rabbitmq');
const axios = require('axios');

const router = express.Router();

const verifyToken = async (token) => {
  try {
    const response = await axios.post('http://auth-service:3000/auth/verify', { token });
    return response.data;
  } catch (error) {
    console.error('Error verifying token:', error);
    return { valid: false };
  }
};

router.post('', async (req, res) => {
  const token = req.headers['authorization'];
  if (!token) return res.status(401).json({ error: 'No token provided' });

  const verification = await verifyToken(token);
  if (!verification.valid) return res.status(401).json({ error: 'Invalid token' });

  const { userId } = verification;
  const { bookId } = req.body;

  try {
    const favoriteId = await Favorite.create(userId, bookId);
    
    // Send message to RabbitMQ
    const channel = getChannel();
    channel.sendToQueue('user_preferences_queue', Buffer.from(JSON.stringify({ action: 'add_favorite', userId, bookId })));
    
    res.status(201).json({ message: 'Favorite added successfully', favoriteId });
  } catch (error) {
    console.error('Error adding favorite:', error);
    res.status(500).json({ error: 'Error adding favorite' });
  }
});

router.delete('', async (req, res) => {
  const token = req.headers['authorization'];
  if (!token) return res.status(401).json({ error: 'No token provided' });

  const verification = await verifyToken(token);
  if (!verification.valid) return res.status(401).json({ error: 'Invalid token' });

  const { userId } = verification;
  const { bookId } = req.body;

  try {
    const deletedCount = await Favorite.delete(userId, bookId);
    
    if (deletedCount > 0) {
      // Send message to RabbitMQ
      const channel = getChannel();
      channel.sendToQueue('user_preferences_queue', Buffer.from(JSON.stringify({ action: 'remove_favorite', userId, bookId })));
      
      res.json({ message: 'Favorite removed successfully' });
    } else {
      res.status(404).json({ error: 'Favorite not found' });
    }
  } catch (error) {
    console.error('Error removing favorite:', error);
    res.status(500).json({ error: 'Error removing favorite' });
  }
});

router.get('', async (req, res) => {
  const token = req.headers['authorization'];
  if (!token) return res.status(401).json({ error: 'No token provided' });

  const verification = await verifyToken(token);
  if (!verification.valid) return res.status(401).json({ error: 'Invalid token' });

  const { userId } = verification;

  try {
    const favorites = await Favorite.findByUser(userId);
    res.json(favorites);
  } catch (error) {
    console.error('Error fetching favorites:', error);
    res.status(500).json({ error: 'Error fetching favorites' });
  }
});

module.exports = router;