// user-preferences-service/src/models/favorite.js
const { pool } = require('../config/database');

class Favorite {
  static async addFavorite(userId, bookId) {
    const query = 'INSERT INTO user_favorites(user_id, book_id) VALUES($1, $2)';
    const values = [userId, bookId];
    await pool.query(query, values);
  }

  static async removeFavorite(userId, bookId) {
    const query = 'DELETE FROM user_favorites WHERE user_id = $1 AND book_id = $2';
    const values = [userId, bookId];
    await pool.query(query, values);
  }

  static async getFavorites(userId) {
    const query = 'SELECT book_id FROM user_favorites WHERE user_id = $1';
    const values = [userId];
    const result = await pool.query(query, values);
    return result.rows.map(row => row.book_id);
  }
}

module.exports = Favorite;