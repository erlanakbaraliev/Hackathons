import { useEffect, useState } from 'react'
import { getPortfolioRisk } from '../api.js'
import { num } from '../format.js'

const SEED_IDS = [1, 2, 3, 4]
const SEED_WEIGHTS = [0.25, 0.25, 0.25, 0.25]

function PortfolioRiskCard() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    getPortfolioRisk(SEED_IDS, SEED_WEIGHTS)
      .then((d) => {
        if (!cancelled) setData(d)
      })
      .catch((e) => {
        if (!cancelled) setError(e.message)
      })
    return () => {
      cancelled = true
    }
  }, [])

  const loading = data === null && !error

  return (
    <section className="card">
      <h2>Portfolio Risk</h2>
      <p className="muted">Equal-weighted: bonds {SEED_IDS.join(', ')}</p>
      {loading && <p className="status">Loading…</p>}
      {error && <p className="error">Failed to load portfolio risk: {error}</p>}
      {data && (
        <div className="metrics">
          <div className="metric">
            <span className="metric-label">Portfolio Duration</span>
            <span className="metric-value">{num(data.portfolio_duration)}</span>
          </div>
          <div className="metric">
            <span className="metric-label">Portfolio Convexity</span>
            <span className="metric-value">{num(data.portfolio_convexity)}</span>
          </div>
        </div>
      )}
    </section>
  )
}

export default PortfolioRiskCard
