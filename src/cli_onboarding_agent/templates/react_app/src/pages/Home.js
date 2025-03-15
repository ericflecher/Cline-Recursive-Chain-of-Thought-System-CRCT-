import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="home-page">
      <h1>Welcome to {{project_name}}</h1>
      <p>{{description}}</p>
      
      <div className="features">
        <h2>Features</h2>
        <ul>
          <li>Modern React application with React 18</li>
          <li>React Router for navigation</li>
          <li>ESLint and Prettier for code quality</li>
          <li>Testing setup with Jest and React Testing Library</li>
        </ul>
      </div>
      
      <div className="cta">
        <Link to="/about" className="btn btn-primary">Learn More</Link>
      </div>
    </div>
  );
}

export default Home;
