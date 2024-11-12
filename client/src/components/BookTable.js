// src/components/BookTable.js
import React from 'react';

const BookTable = ({ books }) => (
  <table>
    <thead>
      <tr>
        <th>Title</th>
        <th>Author</th>
        <th>ISBN</th>
      </tr>
    </thead>
    <tbody>
      {books.map((book) => (
        <tr key={book.id}>
          <td>{book.title}</td>
          <td>{book.author}</td>
          <td>{book.isbn}</td>
        </tr>
      ))}
    </tbody>
  </table>
);

export default BookTable;
