import { Link } from 'react-router-dom';
import { FiUploadCloud, FiActivity, FiFileText, FiTrendingUp, FiCheckCircle, FiShare2 } from 'react-icons/fi';

export default function Home() {
  return (
    <div className="page">
      <section className="hero glass fade-in neon-glow">
        <h1 className="page-title">ChemViz</h1>
        <p className="page-subtitle">
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
      </section>

      <section className="feature-grid">
        <div className="feature-card glass glow-hover fade-in neon-glow">
          <h2 className="section-title center-text">
            <FiActivity className="inline-icon" />
            Real-Time Insights
          </h2>
          <p className="feature-text">
            Track flowrate, pressure, and temperature trends with instant visual
            feedback.
          </p>
        </div>
        <div className="feature-card glass glow-hover fade-in neon-glow">
          <h2 className="section-title center-text">
            <FiUploadCloud className="inline-icon" />
            Structured Uploads
          </h2>
          <p className="feature-text">
            Validate CSV data automatically and keep your datasets clean and
            ready for analysis.
          </p>
        </div>
        <div className="feature-card glass glow-hover fade-in neon-glow">
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

      <section className="stats-row glass fade-in neon-glow">
        <div className="stat-block">
          <span className="stat-value">5</span>
          <span className="stat-label">Recent Uploads</span>
        </div>
        <div className="stat-block">
          <span className="stat-value">3</span>
          <span className="stat-label">Key Metrics</span>
        </div>
        <div className="stat-block">
          <span className="stat-value">100%</span>
          <span className="stat-label">CSV Validation</span>
        </div>
      </section>

      <section className="home-split">
        <div className="split-card glass fade-in neon-glow">
          <h2 className="section-title center-text">Built for Lab Teams</h2>
          <p className="feature-text">
            Centralize equipment data, track performance shifts, and keep
            compliance reporting tight with automated summaries.
          </p>
          <div className="split-highlights">
            <span>Automated analytics</span>
            <span>PDF reports</span>
            <span>Token-secured APIs</span>
          </div>
        </div>
        <div className="split-card glass fade-in neon-glow">
          <h2 className="section-title center-text">Designed for Clarity</h2>
          <p className="feature-text">
            A focused dashboard keeps key metrics visible while minimizing
            visual noise. Stay on top of what matters.
          </p>
          <div className="split-metrics">
            <div>
              <strong>3</strong>
              <span>core metrics</span>
            </div>
            <div>
              <strong>5</strong>
              <span>latest datasets</span>
            </div>
            <div>
              <strong>1</strong>
              <span>PDF export</span>
            </div>
          </div>
        </div>
      </section>

      <section className="timeline glass fade-in neon-glow">
        <h2 className="section-title center-text">How ChemViz Works</h2>
        <div className="workflow-grid">
          <div className="workflow-step">
            <span className="workflow-index">01</span>
            <h3>
              <FiCheckCircle className="inline-icon" />
              Ingest & Validate
            </h3>
            <p>
              Upload standardized CSV datasets. ChemViz validates column schema
              and data integrity before processing.
            </p>
          </div>
          <div className="workflow-step">
            <span className="workflow-index">02</span>
            <h3>
              <FiActivity className="inline-icon" />
              Analyze & Summarize
            </h3>
            <p>
              Compute equipment totals, averages, and distribution metrics with
              fast, repeatable analytics.
            </p>
          </div>
          <div className="workflow-step">
            <span className="workflow-index">03</span>
            <h3>
              <FiShare2 className="inline-icon" />
              Report & Share
            </h3>
            <p>
              Generate PDF-ready reports and share insights with teams and
              stakeholders in seconds.
            </p>
          </div>
        </div>
      </section>

      <section className="cta glass fade-in neon-glow ">
        <h2 className="section-title center-text">
          Ready to visualize your data?
        </h2>
        <p className="feature-text center-text">
          Build a reliable equipment monitoring workflow in minutes.
        </p>
        <div className="hero-actions ">
          <Link className="nav-button" to="/register">
            Create Account
          </Link>
          <Link className="nav-link" to="/login">
            Sign In
          </Link>
        </div>
      </section>
    </div>
  );
}
