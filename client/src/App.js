// src/App.js
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Home from './pages/Home';
import Welcome from './pages/Welcome';

const App = () => {
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  const handleLogout = () => {
    setToken(null);
  };

  return (
    <Router>
      <Switch>
        <Route exact path="/">
          {token ? <Home onLogout={handleLogout} /> : <Welcome />}
        </Route>
        <Route path="/login">
          {token ? <Redirect to="/" /> : <Login setToken={setToken} />}
        </Route>
        <Route path="/register">
          {token ? <Redirect to="/" /> : <Register />}
        </Route>
      </Switch>
    </Router>
  );
};
export default App;