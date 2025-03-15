import React from 'react';

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <p>&copy; {new Date().getFullYear()} {{project_name}}. All rights reserved.</p>
          <p>Created by {{author}}</p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
