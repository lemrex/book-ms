// src/components/BookUpload.js
import React, { useState } from 'react';
import { addBook } from '../services/api';

const BookUpload = ({ onBookAdded }) => {
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [isbn, setIsbn] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await addBook({ title, author, isbn });
      setTitle('');
      setAuthor('');
      setIsbn('');
      onBookAdded();
    } catch (error) {
      console.error('Error adding book:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Title"
        required
      />
      <input
        type="text"
        value={author}
        onChange={(e) => setAuthor(e.target.value)}
        placeholder="Author"
        required
      />
      <input
        type="text"
        value={isbn}
        onChange={(e) => setIsbn(e.target.value)}
        placeholder="ISBN"
        required
      />
      <button type="submit">Add Book</button>
    </form>
  );
};

export default BookUpload;