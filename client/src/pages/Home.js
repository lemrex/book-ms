// src/pages/Home.js
import React, { useState, useEffect } from 'react';
import BookTable from '../components/BookTable';
import BookUpload from '../components/BookUpload';
import { getBooks } from '../services/api';

const Home = ({ onLogout }) => {
  const [books, setBooks] = useState([]);

  const fetchBooks = async () => {
    try {
      const fetchedBooks = await getBooks();
      setBooks(fetchedBooks);
    } catch (error) {
      console.error('Error fetching books:', error);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  return (
    <div>
      <h1>Book Management</h1>
      <button onClick={onLogout}>Logout</button>
      <BookUpload onBookAdded={fetchBooks} />
      <BookTable books={books} />
    </div>
  );
};

export default Home;