// src/pages/Login.tsx

import React, { useState } from 'react';
import { useLogin } from '../api/auth';
import { AxiosError } from 'axios';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  
  // Using the custom hook
  const { mutate: login, isLoading, isError, error } = useLogin();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Call the login mutation
    login({ username, password });
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
      </form>

      {isError && <p>Error: {error instanceof AxiosError ? error.message : 'Login failed'}</p>}
    </div>
  );
};

export default Login;
