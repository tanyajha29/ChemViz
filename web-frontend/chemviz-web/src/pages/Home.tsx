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
      {/* Animated background */}
      <div className="bg-shape shape-1" />
      <div className="bg-shape shape-2" />

      {/* ================= HERO ================= */}
      <section className="home-hero glass neon-glow fade-in">
        <div className="container home-hero-content">
          <h1 className="home-title">ChemViz</h1>
          <p className="home-subtitle">
            Professional data monitoring for chemical equipment.
            Upload, analyze, and visualize datasets with confidence.
          </p>

          <div className="hero-actions">
            <Link className="nav-button" to="/upload">
              <FiUploadCloud />
              Upload CSV
            </Link>
            <Link className="nav-link" to="/dashboard">
              <FiTrendingUp />
              Dashboard
            </Link>
          </div>
        </div>
      </section>

      {/* ================= FEATURES ================= */}
      <section className="home-section fade-in fade-delay-1">
        <div className="container">
          <div className="home-section-header">
            <h2 className="section-title">Core Features</h2>
            <p className="feature-text">
              Purpose-built tools for ingestion, analytics, and reporting.
            </p>
          </div>

          <div className="home-grid">
            <div className="home-card glass neon-glow">
              <FiActivity className="feature-icon" />
              <h3>Real-Time Insights</h3>
              <p>
                Monitor flowrate, pressure, and temperature trends with instant
                visual feedback.
              </p>
            </div>

            <div className="home-card glass neon-glow">
              <FiUploadCloud className="feature-icon" />
              <h3>Structured Uploads</h3>
              <p>
                Automatic CSV validation keeps your datasets clean and
                analysis-ready.
              </p>
            </div>

            <div className="home-card glass neon-glow">
              <FiFileText className="feature-icon" />
              <h3>Report Ready</h3>
              <p>
                Generate PDF reports with summary analytics in a single click.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ================= WORKFLOW ================= */}
      <section className="home-section fade-in fade-delay-2">
        <div className="container">
          <div className="home-section-header">
            <h2 className="section-title">How It Works</h2>
            <p className="feature-text">
              A simple, repeatable pipeline for reliable analytics.
            </p>
          </div>

          <div className="home-grid">
            <div className="home-card glass neon-glow workflow-card">
              <span className="workflow-index">01</span>
              <h3>
                <FiCheckCircle /> Ingest & Validate
              </h3>
              <p>
                Upload standardized datasets and validate required columns
                automatically.
              </p>
            </div>

            <div className="home-card glass neon-glow workflow-card">
              <span className="workflow-index">02</span>
              <h3>
                <FiActivity /> Analyze & Summarize
              </h3>
              <p>
                Compute totals, averages, and distributions with repeatable
                analytics.
              </p>
            </div>

            <div className="home-card glass neon-glow workflow-card">
              <span className="workflow-index">03</span>
              <h3>
                <FiShare2 /> Report & Share
              </h3>
              <p>
                Generate PDF-ready reports and share insights with your team.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ================= STATS ================= */}
      <section className="home-section fade-in fade-delay-3">
        <div className="container">
          <div className="home-section-header">
            <h2 className="section-title center-text">At a Glance</h2>
            <p className="feature-text center-text">
              Simple, repeatable analytics without data overload.
            </p>
          </div>
          <div className="home-metrics">
            <div className="metric-card glass neon-glow">
              <span className="metric-value">5</span>
              <span className="metric-label">Datasets / User</span>
            </div>
            <div className="metric-card glass neon-glow">
              <span className="metric-value">3</span>
              <span className="metric-label">Equipment Metrics</span>
            </div>
            <div className="metric-card glass neon-glow">
              <span className="metric-value">PDF</span>
              <span className="metric-label">One-Click Reports</span>
            </div>
          </div>
        </div>
      </section>

      {/* ================= CTA ================= */}
      <section className="home-cta glass neon-glow fade-in fade-delay-4">
        <div className="container center-text">
          <h2 className="section-title">Ready to visualize your data?</h2>
          <p className="feature-text">
            Build a reliable equipment monitoring workflow in minutes.
          </p>

          <div className="hero-actions">
            <Link className="nav-button" to="/register">
              Create Account
            </Link>
            <Link className="nav-link" to="/login">
              Sign In
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
