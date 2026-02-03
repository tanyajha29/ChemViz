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

import { DatasetSummary, fetchSummaries } from '../api/datasets';

ChartJS.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

export default function Dashboard() {
  const [summary, setSummary] = useState<DatasetSummary | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    let isMounted = true;
    fetchSummaries()
      .then((results) => {
        if (!isMounted) {
          return;
        }
        setSummary(results[0]?.summary ?? null);
      })
      .catch(() => {
        if (!isMounted) {
          return;
        }
        setError('Failed to load summary data.');
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const typeDistributionData = useMemo(() => {
    if (!summary) {
      return null;
    }
    const labels = Object.keys(summary.type_distribution ?? {});
    const values = Object.values(summary.type_distribution ?? {});
    return {
      labels,
      datasets: [
        {
          label: 'Equipment Type Count',
          data: values,
          backgroundColor: '#4A90E2',
        },
      ],
    };
  }, [summary]);

  const averagesData = useMemo(() => {
    if (!summary) {
      return null;
    }
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
          backgroundColor: ['#7ED321', '#F5A623', '#BD10E0'],
        },
      ],
    };
  }, [summary]);

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Overview charts and summary metrics.</p>
      {error ? <p>{error}</p> : null}
      {!summary ? <p>Loading summary...</p> : null}
      {summary && typeDistributionData ? (
        <div>
          <h2>Equipment Type Distribution</h2>
          <Bar data={typeDistributionData} />
        </div>
      ) : null}
      {summary && averagesData ? (
        <div>
          <h2>Average Metrics</h2>
          <Bar data={averagesData} />
        </div>
      ) : null}
    </div>
  );
}
