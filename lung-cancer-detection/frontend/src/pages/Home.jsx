import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home-container">
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            Next-Gen <span className="highlight">Lung Cancer</span> Detection
          </h1>
          <p className="hero-description">
            Leveraging advanced Deep Learning and Computer Vision to assist medical professionals in early-stage lung nodule analysis.
          </p>
          <div className="hero-actions">
            <Link to="/dashboard" className="primary-btn">
              Get Started
            </Link>
            <Link to="/about" className="secondary-btn">
              Learn More
            </Link>
          </div>
        </div>
        <div className="hero-visual">
          <div className="visual-background"></div>
          <div className="visual-image">
            {/* An abstract representation of a scan or AI processing */}
            <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
              <path fill="#3B82F6" d="M44.7,-76.4C58.8,-69.2,71.8,-59.1,79.6,-45.8C87.4,-32.5,90,-16.2,88.5,-0.9C86.9,14.5,81.2,28.9,72.4,41.4C63.6,53.9,51.7,64.4,38,71.1C24.3,77.8,8.8,80.7,-5.7,78.2C-20.2,75.7,-33.7,67.8,-45.8,59C-57.9,50.1,-68.6,40.3,-75.4,28C-82.2,15.7,-85.1,1,-83.4,-13.2C-81.7,-27.4,-75.4,-41.1,-65.4,-51.7C-55.4,-62.4,-41.7,-70.1,-28.1,-77.2C-14.5,-84.3,-1,-90.7,13.5,-88.7C28.1,-86.7,42.2,-76.4,44.7,-76.4Z" transform="translate(100 100)" />
              <circle cx="100" cy="100" r="40" fill="white" opacity="0.3" />
              <rect x="80" y="80" width="40" height="40" fill="white" opacity="0.2" />
            </svg>
          </div>
        </div>
      </section>

      <section className="features-grid">
        <div className="feature-card">
          <div className="feature-icon">🔍</div>
          <h3>High Precision</h3>
          <p>Utilizes ResNet50 architecture for state-of-the-art nodule classification accuracy.</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">⚡</div>
          <h3>Real-time Analysis</h3>
          <p>Instantaneous processing of CT scans with clear diagnostic probabilities.</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">🧠</div>
          <h3>Explainable AI</h3>
          <p>Integrated Grad-CAM visualization to highlight specific regions of interest for doctors.</p>
        </div>
      </section>

      <section className="cta-section">
        <h2>Ready to assist your diagnosis?</h2>
        <p>Join physicians using AI to improve patient outcomes today.</p>
        <Link to="/dashboard" className="cta-btn">Open Radiology Dashboard</Link>
      </section>
    </div>
  );
};

export default Home;
