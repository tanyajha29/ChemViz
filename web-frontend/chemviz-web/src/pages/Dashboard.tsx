import { useEffect, useMemo, useState } from 'react';
import { Bar, Doughnut } from 'react-chartjs-2';
import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  PointElement,
  LineElement,
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

import { DatasetSummary, fetchLatestRows, fetchSummaries, LatestDataset } from '../api/datasets';

const percentLabelPlugin = {
  id: 'percentLabel',
  afterDatasetDraw(chart: ChartJS, _args: unknown, pluginOptions: any) {
    const { ctx, data } = chart;
    const dataset = data.datasets?.[0];
    if (!dataset) return;
    const values = (dataset.data as Array<number | null | undefined>).map((v) =>
      typeof v === 'number' ? v : Number(v)
    );
    const total = values.reduce((sum, value) => sum + (Number.isFinite(value) ? value : 0), 0);
    if (!total) return;
    const meta = chart.getDatasetMeta(0);
    const minPercent = typeof pluginOptions?.minPercent === 'number' ? pluginOptions.minPercent : 4;

    meta.data.forEach((element, index) => {
      const raw = values[index] ?? 0;
      if (!Number.isFinite(raw) || raw <= 0) return;
      const percent = (raw / total) * 100;
      if (percent < minPercent) return;
      const { x, y } = (element as any).tooltipPosition();

      ctx.save();
      ctx.fillStyle = pluginOptions?.color ?? '#EAF6FF';
      ctx.font = '600 12px Manrope, system-ui';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`${percent.toFixed(0)}%`, x, y);
      ctx.restore();
    });
  },
};

ChartJS.register(
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  percentLabelPlugin
);

export default function Dashboard() {
  const [summary, setSummary] = useState<DatasetSummary | null>(null);
  const [uploadsCount, setUploadsCount] = useState(0);
  const [error, setError] = useState('');
  const [latestRows, setLatestRows] = useState<LatestDataset | null>(null);
  const [metric, setMetric] = useState<'Flowrate' | 'Pressure' | 'Temperature'>(
    'Flowrate'
  );

  const loadSummary = () => {
    setError('');
    fetchSummaries()
      .then((results) => {
        setUploadsCount(results.length);
        setSummary(results[0]?.summary ?? null);
      })
      .catch(() => {
        setError('Failed to load summary data.');
      });
  };

  const loadLatestRows = () => {
    fetchLatestRows()
      .then((data) => setLatestRows(data))
      .catch(() => setLatestRows(null));
  };

  useEffect(() => {
    loadSummary();
    loadLatestRows();
    const handler = () => {
      loadSummary();
      loadLatestRows();
    };
    window.addEventListener('datasets:updated', handler);
    return () => window.removeEventListener('datasets:updated', handler);
  }, []);

  const formatMetric = (value: number | null | undefined, decimals = 2) => {
    if (value === null || value === undefined || Number.isNaN(value)) return '—';
    return new Intl.NumberFormat('en-US', {
      maximumFractionDigits: decimals,
    }).format(value);
  };

  const formatCount = (value: number | null | undefined) => {
    if (value === null || value === undefined || Number.isNaN(value)) return '—';
    return new Intl.NumberFormat('en-US', {
      maximumFractionDigits: 0,
    }).format(value);
  };

  const typeDistributionData = useMemo(() => {
    if (!summary) return null;
    const labels = Object.keys(summary.type_distribution ?? {});
    const values = Object.values(summary.type_distribution ?? {});
    const palette = [
      'rgba(79, 172, 254, 0.75)',
      'rgba(124, 58, 237, 0.7)',
      'rgba(245, 158, 11, 0.7)',
      'rgba(16, 185, 129, 0.7)',
      'rgba(236, 72, 153, 0.7)',
      'rgba(59, 130, 246, 0.7)',
    ];
    return {
      labels,
      datasets: [
        {
          label: 'Equipment Count',
          data: values,
          backgroundColor: labels.map((_, idx) => palette[idx % palette.length]),
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

  const deepDiveData = useMemo(() => {
    if (!latestRows?.rows?.length) return null;
    const values = latestRows.rows
      .map((row) => ({
        name: row['Equipment Name'],
        value: Number(row[metric]),
      }))
      .filter((item) => !Number.isNaN(item.value));

    const top = values.sort((a, b) => b.value - a.value).slice(0, 20);

    return {
      labels: top.map((item) => item.name),
      datasets: [
        {
          label: metric,
          data: top.map((item) => item.value),
          backgroundColor: 'rgba(56, 189, 248, 0.7)',
          borderRadius: 6,
        },
      ],
    };
  }, [latestRows, metric]);

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

  const doughnutOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: { color: '#EAF6FF' },
      },
      percentLabel: {
        color: '#EAF6FF',
        minPercent: 4,
      },
    },
  };

  return (
    <div className="page gradient-bg dashboard-page">
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
          value={formatCount(summary?.total_equipment ?? null)}
        />
        <SummaryCard
          icon={<FiTrendingUp />}
          label="Avg Flowrate"
          value={formatMetric(summary?.avg_flowrate ?? null)}
        />
        <SummaryCard
          icon={<FiActivity />}
          label="Avg Pressure"
          value={formatMetric(summary?.avg_pressure ?? null)}
        />
        <SummaryCard
          icon={<FiThermometer />}
          label="Avg Temperature"
          value={formatMetric(summary?.avg_temperature ?? null)}
        />
        <SummaryCard
          icon={<FiDatabase />}
          label="Datasets Stored"
          value={formatCount(uploadsCount)}
        />
      </section>

      {/* CHARTS */}
      <section className="charts-grid">
        <div className="chart-card glass glow-hover fade-in neon-glow">
          <h2 className="section-title">Equipment Type Distribution</h2>
          {summary && typeDistributionData ? (
            <Doughnut data={typeDistributionData} options={doughnutOptions} />
          ) : (
            <p className="empty-state">Upload a CSV to visualize equipment types.</p>
          )}
        </div>

        <div className="chart-card glass glow-hover fade-in neon-glow">
          <h2 className="section-title">Average Parameters</h2>
          {summary && averagesData ? (
            <Bar data={averagesData} options={chartOptions} />
          ) : (
            <p className="empty-state">Upload a CSV to view averages.</p>
          )}
        </div>
      </section>

      {/* DEEP DIVE */}
      <section className="chart-card glass glow-hover fade-in neon-glow">
        <h2 className="section-title">Single Metric Deep Dive</h2>
        <div className="metric-toggle">
          {(['Flowrate', 'Pressure', 'Temperature'] as const).map((item) => (
            <button
              key={item}
              type="button"
              className={`metric-pill ${metric === item ? 'active' : ''}`}
              onClick={() => setMetric(item)}
            >
              {item}
            </button>
          ))}
        </div>
        {deepDiveData ? (
          <Bar data={deepDiveData} options={chartOptions} />
        ) : (
          <p className="empty-state">Upload a CSV to explore a metric.</p>
        )}
      </section>

      {/* TABLE PLACEHOLDER */}
      <section className="table-card glass fade-in neon-glow">
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
            {latestRows?.rows?.length ? (
              latestRows.rows.slice(0, 10).map((row) => (
                <tr key={`${row['Equipment Name']}-${row.Type}`}>
                  <td>{row['Equipment Name']}</td>
                  <td>{row.Type}</td>
                  <td>{row.Flowrate}</td>
                  <td>{row.Pressure}</td>
                  <td>{row.Temperature}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={5} className="empty-state">
                  Upload a CSV to populate this table.
                </td>
              </tr>
            )}
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
    <div className="summary-card glass glow-hover fade-in neon-glow">
      <div className="summary-icon">{icon}</div>
      <span className="summary-label">{label}</span>
      <span className="summary-value">{value}</span>
    </div>
  );
}
