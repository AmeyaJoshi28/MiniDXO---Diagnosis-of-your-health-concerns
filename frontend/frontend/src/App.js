import React, { useState, useEffect } from 'react';
import ChatBox from './ChatBox';
import './App.css';

function App() {
  const [reasoning, setReasoning] = useState('Awaiting patient data...');
  const [confidence, setConfidence] = useState({});

  const handleResponse = (data) => {
    // This updates the sidebar when ChatBox gets a response from the API
    setReasoning(data.reasoning);
    setConfidence(data.confidence || {});
  };

  useEffect(() => {
    // Reset session on load to clear 404 errors and old data
    fetch('http://localhost:8000/reset', { method: 'POST' })
      .catch(err => console.log("Backend offline"));
  }, []);

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1>
            MiniDXO <span className="header-sub">| Diagnosis of your health concerns</span>
          </h1>
          <div className="status-badge">AI Systems Active</div>
        </div>
      </header>

      <div className="main-layout">
        {/* Left: Interactive Chat */}
        <ChatBox onResponse={handleResponse} />

        {/* Right: Diagnostic Metadata */}
        <aside className="sidebar">
          <div className="card">
            <h3>Internal Monologue</h3>
            <div className="reasoning-box" dangerouslySetInnerHTML={{ __html: reasoning }} />
          </div>

          <div className="card">
            <h3>Confidence Levels</h3>
            {Object.entries(confidence).length === 0 ? (
              <p className="empty-state">No symptoms identified yet.</p>
            ) : (
              Object.entries(confidence).map(([name, val]) => (
                <div key={name} className="conf-row">
                  <div className="conf-label">
                    <span>{name}</span>
                    <span>{Math.round(val * 100)}%</span>
                  </div>
                  <div className="bar-bg">
                    <div 
                      className="bar-fill" 
                      style={{ 
                        width: `${val * 100}%`,
                        backgroundColor: val > 0.8 ? '#ef4444' : val > 0.5 ? '#f59e0b' : '#10b981'
                      }}
                    ></div>
                  </div>
                </div>
              ))
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}

export default App;