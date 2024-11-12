// user-preferences-service/src/app.js
const express = require('express');
const { favoritesRouter } = require('./routes/favorites');
const { connectDB } = require('./config/database');
const { connectRabbitMQ } = require('./config/rabbitmq');

const app = express();
app.use(express.json());

// Connect to database and RabbitMQ
connectDB();
connectRabbitMQ();

// Use favorites routes
app.use('/favorites', favoritesRouter);

const PORT = process.env.PORT || 3002;
app.listen(PORT, () => console.log(`User Preferences service running on port ${PORT}`));