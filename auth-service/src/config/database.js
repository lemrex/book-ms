// // auth-service/src/config/database.js
// const { Pool } = require('pg');

// const pool = new Pool({
//   user: 'root',
//   host: '111.119.196.15',
//   database: 'inventory',
//   password: '#Qwerty123',
//   port: 5432,
// });

// const connectDB = async () => {
//   try {
//     await pool.connect();
//     console.log('Connected to the bookstore_auth database');
//   } catch (err) {
//     console.error('Failed to connect to the bookstore_auth database', err);
//     process.exit(1);
//   }
// };

// module.exports = { pool, connectDB };


// auth-service/src/config/database.js
const { Pool } = require('pg');
require('dotenv').config(); // Load environment variables from .env file

const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_DATABASE,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
});

const connectDB = async () => {
  try {
    await pool.connect();
    console.log('Connected to the bookstore_auth database');
  } catch (err) {
    console.error('Failed to connect to the bookstore_auth database', err);
    process.exit(1);
  }
};

module.exports = { pool, connectDB };
