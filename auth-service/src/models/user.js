// auth-service/src/models/user.js
const { pool } = require('../config/database');
const bcrypt = require('bcrypt');

class User {
  static async createUser(username, password) {
    const hashedPassword = await bcrypt.hash(password, 10);
    const query = 'INSERT INTO users(username, password) VALUES($1, $2) RETURNING id';
    const values = [username, hashedPassword];
    const result = await pool.query(query, values);
    return result.rows[0].id;
  }

  static async findByUsername(username) {
    const query = 'SELECT * FROM users WHERE username = $1';
    const values = [username];
    const result = await pool.query(query, values);
    return result.rows[0];
  }
}

module.exports = User;