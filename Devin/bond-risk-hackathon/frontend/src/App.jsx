import { useEffect, useState } from 'react'
import './App.css'
import { getBonds } from './api.js'
import YieldCurveChart from './components/YieldCurveChart.jsx'
import PortfolioRiskCard from './components/PortfolioRiskCard.jsx'
import BondTable from './components/BondTable.jsx'

function App() {
  const [bonds, setBonds] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    getBonds()
      .then((data) => {
        if (!cancelled) setBonds(data)
      })
      .catch((e) => {
        if (!cancelled) setError(e.message)
      })
    return () => {
      cancelled = true
    }
  }, [])

  const loading = bonds === null && !error

  return (
    <main className="container">
      <h1>Bond Portfolio Risk Dashboard</h1>
      <YieldCurveChart bonds={bonds} loading={loading} error={error} />
      <PortfolioRiskCard />
      <BondTable bonds={bonds} loading={loading} error={error} />
    </main>
  )
}

export default App
