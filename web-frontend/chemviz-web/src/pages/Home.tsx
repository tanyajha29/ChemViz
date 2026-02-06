import { Link } from 'react-router-dom';
import {
  FiActivity,
  FiCheckCircle,
  FiFileText,
  FiShare2,
  FiTrendingUp,
  FiUploadCloud,
} from 'react-icons/fi';

export default function Home() {
  return (
    <div className="auth-wrapper home-wrapper">
      <div className="bg-shape shape-1" />
      <div className="bg-shape shape-2" />

      <section className="home-hero glass neon-glow">
        <div className="home-hero-content">
          <h1 className="home-title">ChemViz</h1>
          <p className="home-subtitle">
            Data-first monitoring for chemical equipment. Upload, analyze, and
            visualize your datasets with clarity.
          </p>
          <div className="hero-actions">
            <Link className="nav-button" to="/upload">
              <FiUploadCloud className="inline-icon" />
              Upload CSV
            </Link>
            <Link className="nav-link" to="/dashboard">
              <FiTrendingUp className="inline-icon" />
              View Dashboard
            </Link>
          </div>
        </div>
      </section>

      <section className="home-grid">
        <div className="home-card glass neon-glow">
          <h2 className="section-title center-text">
            <FiActivity className="inline-icon" />
            Real-Time Insights
          </h2>
          <p className="feature-text">
            Track flowrate, pressure, and temperature trends with instant visual
            feedback.
          </p>
        </div>
        <div className="home-card glass neon-glow">
          <h2 className="section-title center-text">
            <FiUploadCloud className="inline-icon" />
            Structured Uploads
          </h2>
          <p className="feature-text">
            Validate CSV data automatically and keep your datasets clean and
            ready for analysis.
          </p>
        </div>
        <div className="home-card glass neon-glow">
          <h2 className="section-title center-text">
            <FiFileText className="inline-icon" />
            Report Ready
          </h2>
          <p className="feature-text">
            Generate PDF reports with summary analytics and structured tables in
            one click.
          </p>
        </div>
      </section>

      <section className="home-grid">
        <div className="home-card glass neon-glow">
          <span className="workflow-index">01</span>
          <h3>
            <FiCheckCircle className="inline-icon" />
            Ingest & Validate
          </h3>
          <p>
            Upload standardized CSV datasets and validate required columns
            before analysis.
          </p>
        </div>
        <div className="home-card glass neon-glow">
          <span className="workflow-index">02</span>
          <h3>
            <FiActivity className="inline-icon" />
            Analyze & Summarize
          </h3>
          <p>
            Compute totals, averages, and distributions with repeatable
            analytics.
          </p>
        </div>
        <div className="home-card glass neon-glow">
          <span className="workflow-index">03</span>
          <h3>
            <FiShare2 className="inline-icon" />
            Report & Share
          </h3>
          <p>
            Generate PDF-ready reports and share insights with your team.
          </p>
        </div>
      </section>

      <section className="home-cta glass neon-glow">
        <h2 className="section-title center-text">Ready to visualize your data?</h2>
        <p className="feature-text center-text">
          Build a reliable equipment monitoring workflow in minutes.
        </p>
        <div className="hero-actions">
          <Link className="nav-button" to="/register">Create Account</Link>
          <Link className="nav-link" to="/login">Sign In</Link>
        </div>
      </section>
    </div>
  );
}
