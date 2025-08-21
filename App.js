import React, { useState } from 'react';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(null);
    setError('');

    try {
      const response = await fetch('http://localhost:5000/check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url })
      });

      const data = await response.json();
      if (!response.ok) {
        setError(data.message || 'Something went wrong');
      } else {
        setResult(data);
      }
    } catch (err) {
      setError('Server not reachable');
    }
  };

  return (
    <div className="container">
      <h1>🔒 Phishing URL Checker</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter URL (e.g., https://example.com)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
        />
        <button type="submit">Check URL</button>
      </form>

      {result && (
        <div className={`result ${result.phishing ? 'danger' : 'safe'}`}>
          <h2>{result.message}</h2>
        </div>
      )}

      {error && <div className="error">{error}</div>}
    </div>
  );
}

export default App;

