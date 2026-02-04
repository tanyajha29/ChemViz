import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="page">
      <section className="hero glass fade-in">
        <h1 className="page-title">ChemViz</h1>
        <p className="page-subtitle">
          Data-first monitoring for chemical equipment. Upload, analyze, and
          visualize your datasets with clarity.
        </p>
        <div className="hero-actions">
          <Link className="nav-button" to="/upload">
            Upload CSV
          </Link>
          <Link className="nav-link" to="/dashboard">
            View Dashboard
          </Link>
        </div>
      </section>

      <section className="feature-grid">
        <div className="feature-card glass glow-hover fade-in">
          <h2 className="section-title">Real-Time Insights</h2>
          <p className="feature-text">
            Track flowrate, pressure, and temperature trends with instant visual
            feedback.
          </p>
        </div>
        <div className="feature-card glass glow-hover fade-in">
          <h2 className="section-title">Structured Uploads</h2>
          <p className="feature-text">
            Validate CSV data automatically and keep your datasets clean and
            ready for analysis.
          </p>
        </div>
        <div className="feature-card glass glow-hover fade-in">
          <h2 className="section-title">Report Ready</h2>
          <p className="feature-text">
            Generate PDF reports with summary analytics and structured tables in
            one click.
          </p>
        </div>
      </section>

      <section className="stats-row glass fade-in">
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

      <section className="timeline glass fade-in">
        <h2 className="section-title">How ChemViz Works</h2>
        <ol className="timeline-list">
          <li>
            <span className="timeline-step">1</span>
            Upload equipment CSVs with standardized columns.
          </li>
          <li>
            <span className="timeline-step">2</span>
            Review summary analytics and distributions instantly.
          </li>
          <li>
            <span className="timeline-step">3</span>
            Export polished PDF reports for teams and audits.
          </li>
        </ol>
      </section>

      <section className="cta glass fade-in">
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
      </section>
    </div>
  );
}
