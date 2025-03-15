import React from 'react';
import { Link } from 'react-router-dom';

function About() {
  return (
    <div className="about-page">
      <h1>About {{project_name}}</h1>
      <p>{{description}}</p>
      
      <div className="about-content">
        <h2>Project Information</h2>
        <p>This project was created using the CLI Onboarding Agent's React template.</p>
        <p>Version: {{version}}</p>
        <p>Author: {{author}}</p>
      </div>
      
      <div className="tech-stack">
        <h2>Technology Stack</h2>
        <ul>
          <li>React 18</li>
          <li>React Router</li>
          <li>ESLint & Prettier</li>
          <li>Jest & React Testing Library</li>
        </ul>
      </div>
      
      <div className="cta">
        <Link to="/" className="btn btn-secondary">Back to Home</Link>
      </div>
    </div>
  );
}

export default About;
