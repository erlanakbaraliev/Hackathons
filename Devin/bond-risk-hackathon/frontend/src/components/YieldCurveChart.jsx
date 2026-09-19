import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

function YieldCurveChart({ bonds, loading, error }) {
  if (loading) {
    return (
      <section className="card">
        <h2>Yield Curve</h2>
        <p className="status">Loading…</p>
      </section>
    )
  }
  if (error) {
    return (
      <section className="card">
        <h2>Yield Curve</h2>
        <p className="error">Failed to load bonds: {error}</p>
      </section>
    )
  }

  const data = [...bonds]
    .sort((a, b) => a.maturity_years - b.maturity_years)
    .map((b) => ({
      name: b.name,
      maturity: b.maturity_years,
      ytm: +(b.ytm * 100).toFixed(2),
    }))

  return (
    <section className="card">
      <h2>Yield Curve</h2>
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={data} margin={{ top: 16, right: 24, bottom: 24, left: 8 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="maturity"
            type="number"
            domain={[0, 'dataMax']}
            label={{ value: 'Maturity (years)', position: 'insideBottom', offset: -12 }}
          />
          <YAxis
            dataKey="ytm"
            domain={['auto', 'auto']}
            label={{
              value: 'Yield to Maturity (%)',
              angle: -90,
              position: 'insideLeft',
              style: { textAnchor: 'middle' },
            }}
            tickFormatter={(v) => v.toFixed(1)}
          />
          <Tooltip
            formatter={(v) => [`${v.toFixed(2)}%`, 'YTM']}
            labelFormatter={(v) => `Maturity: ${v}y`}
          />
          <Line
            type="monotone"
            dataKey="ytm"
            stroke="#2563eb"
            strokeWidth={2}
            dot={{ r: 5, fill: '#2563eb' }}
            activeDot={{ r: 7 }}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </section>
  )
}

export default YieldCurveChart
