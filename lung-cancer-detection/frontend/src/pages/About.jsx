import React from 'react';
import './About.css';

const About = () => {
  return (
    <div className="about-page">
      <div className="about-hero">
        <h1>AI-Powered Lung Cancer Diagnostics</h1>
        <p className="hero-subtitle">
          Empowering radiologists and oncologists with rapid, accurate 
          Deep Learning analysis of CT imaging.
        </p>
      </div>

      <div className="about-content">
        <section className="info-section">
          <div className="icon-wrapper">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
          </div>
          <h2>Our Mission</h2>
          <p>
            Lung cancer is the leading cause of cancer death worldwide, yet early 
            detection can drastically improve survival rates. This platform leverages 
            state-of-the-art Computer Vision to assist medical professionals by 
            highlighting suspicious nodules, acting as an intelligent second opinion.
          </p>
        </section>

        <section className="info-section">
          <div className="icon-wrapper">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
              <polyline points="2 17 12 22 22 17"></polyline>
              <polyline points="2 12 12 17 22 12"></polyline>
            </svg>
          </div>
          <h2>The Technology</h2>
          <p>
            Built on a <strong>ResNet50 Architecture</strong> originally trained on the ImageNet dataset, 
            our model utilizes Transfer Learning customized for medical imaging. The pipeline applies 
            Contrast Limited Adaptive Histogram Equalization <em>(CLAHE)</em> to raw CT scans to maximize 
            tissue contrast before passing it through our binary classifier (Benign vs. Malignant).
          </p>
        </section>

        <section className="info-section">
          <div className="icon-wrapper">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
          </div>
          <h2>Clinical Disclaimer</h2>
          <p className="disclaimer-text">
            This tool is designed strictly for research, educational, and assistive purposes. 
            It is <strong>not</strong> a replacement for professional clinical judgment. 
            Final diagnoses and treatment plans must always be decided by certified medical 
            personnel following standard biopsy and oncology protocols.
          </p>
        </section>
      </div>
      
      <div className="team-section">
        <h3>Project Repository</h3>
        <p>Built as an open-source medical AI initiative.</p>
        <a href="https://github.com" target="_blank" rel="noreferrer" className="github-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
          </svg>
          View Source Code
        </a>
      </div>
    </div>
  );
};

export default About;
