import { useEffect, useMemo, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Title,
  Tooltip,
} from 'chart.js';
import {
  FiBox,
  FiTrendingUp,
  FiActivity,
  FiThermometer,
  FiDatabase,
} from 'react-icons/fi';

import { DatasetSummary, fetchSummaries } from '../api/datasets';

ChartJS.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

export default function Dashboard() {
  const [summary, setSummary] = useState<DatasetSummary | null>(null);
  const [uploadsCount, setUploadsCount] = useState(0);
  const [error, setError] = useState('');

  useEffect(() => {
    let isMounted = true;
    fetchSummaries()
      .then((results) => {
        if (!isMounted) return;
        setUploadsCount(results.length);
        setSummary(results[0]?.summary ?? null);
      })
      .catch(() => {
        if (!isMounted) return;
        setError('Failed to load summary data.');
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const typeDistributionData = useMemo(() => {
    if (!summary) return null;
    return {
      labels: Object.keys(summary.type_distribution ?? {}),
      datasets: [
        {
          label: 'Equipment Count',
          data: Object.values(summary.type_distribution ?? {}),
          backgroundColor: 'rgba(79, 172, 254, 0.65)',
          borderRadius: 6,
        },
      ],
    };
  }, [summary]);

  const averagesData = useMemo(() => {
    if (!summary) return null;
    return {
      labels: ['Flowrate', 'Pressure', 'Temperature'],
      datasets: [
        {
          label: 'Average',
          data: [
            summary.avg_flowrate ?? 0,
            summary.avg_pressure ?? 0,
            summary.avg_temperature ?? 0,
          ],
          backgroundColor: [
            'rgba(126, 211, 33, 0.7)',
            'rgba(245, 166, 35, 0.7)',
            'rgba(189, 16, 224, 0.7)',
          ],
          borderRadius: 6,
        },
      ],
    };
  }, [summary]);

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { labels: { color: '#EAF6FF' } },
    },
    scales: {
      x: { ticks: { color: '#A8C7D8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
      y: { ticks: { color: '#A8C7D8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
    },
  };

  return (
    <div className="page gradient-bg">
      <header className="page-header fade-in">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">
          Real-time insights from your chemical equipment datasets.
        </p>
      </header>

      {error && <p className="error-text">{error}</p>}

      {/* SUMMARY CARDS */}
      <section className="summary-grid">
        <SummaryCard
          icon={<FiBox />}
          label="Total Equipment"
          value={summary?.total_equipment ?? '—'}
        />
        <SummaryCard
          icon={<FiTrendingUp />}
          label="Avg Flowrate"
          value={summary?.avg_flowrate ?? '—'}
        />
        <SummaryCard
          icon={<FiActivity />}
          label="Avg Pressure"
          value={summary?.avg_pressure ?? '—'}
        />
        <SummaryCard
          icon={<FiThermometer />}
          label="Avg Temperature"
          value={summary?.avg_temperature ?? '—'}
        />
        <SummaryCard
          icon={<FiDatabase />}
          label="Datasets Stored"
          value={uploadsCount}
        />
      </section>

      {/* CHARTS */}
      <section className="charts-grid">
        <div className="chart-card glass glow-hover fade-in">
          <h2 className="section-title">Equipment Type Distribution</h2>
          {summary && typeDistributionData ? (
            <Bar data={typeDistributionData} options={chartOptions} />
          ) : (
            <p className="empty-state">Upload a CSV to visualize equipment types.</p>
          )}
        </div>

        <div className="chart-card glass glow-hover fade-in">
          <h2 className="section-title">Average Parameters</h2>
          {summary && averagesData ? (
            <Bar data={averagesData} options={chartOptions} />
          ) : (
            <p className="empty-state">Upload a CSV to view averages.</p>
          )}
        </div>
      </section>

      {/* TABLE PLACEHOLDER */}
      <section className="table-card glass fade-in">
        <h2 className="section-title">Latest Equipment Table</h2>
        <table className="data-table">
          <thead>
            <tr>
              <th>Equipment</th>
              <th>Type</th>
              <th>Flowrate</th>
              <th>Pressure</th>
              <th>Temperature</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td colSpan={5} className="empty-state">
                Upload a CSV to populate this table.
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  );
}

/* ---------------------------------- */
/* Summary Card Component              */
/* ---------------------------------- */

function SummaryCard({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string | number;
}) {
  return (
    <div className="summary-card glass glow-hover fade-in">
      <div className="summary-icon">{icon}</div>
      <span className="summary-label">{label}</span>
      <span className="summary-value">{value}</span>
    </div>
  );
}
