import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="main-nav">
      <div className="nav-container">
        <div className="nav-logo">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="logo-icon">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
          </svg>
          <span className="logo-text">PulmoAI</span>
        </div>
        
        <div className="nav-links">
          <NavLink 
            to="/" 
            className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
            end
          >
            Home
          </NavLink>
          
          <NavLink 
            to="/dashboard" 
            className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
          >
            Dashboard
          </NavLink>
          
          <NavLink 
            to="/about" 
            className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
          >
            About
          </NavLink>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
