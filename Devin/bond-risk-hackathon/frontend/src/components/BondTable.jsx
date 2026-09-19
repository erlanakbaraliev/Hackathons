import { useEffect, useState } from 'react'
import { getBondPrice } from '../api.js'
import { num, pct } from '../format.js'

function BondTable({ bonds, loading, error }) {
  const [prices, setPrices] = useState({})
  const [priceError, setPriceError] = useState(null)

  useEffect(() => {
    if (!bonds) return
    let cancelled = false
    Promise.all(bonds.map((b) => getBondPrice(b.id)))
      .then((results) => {
        if (!cancelled)
          setPrices(Object.fromEntries(results.map((r) => [r.bond_id, r.price])))
      })
      .catch((e) => {
        if (!cancelled) setPriceError(e.message)
      })
    return () => {
      cancelled = true
    }
  }, [bonds])

  return (
    <section className="card">
      <h2>Bonds</h2>
      {loading && <p className="status">Loading…</p>}
      {error && <p className="error">Failed to load bonds: {error}</p>}
      {bonds && !loading && !error && (
        <>
          {priceError && <p className="error">Failed to load prices: {priceError}</p>}
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th className="num">Maturity (years)</th>
                <th className="num">Coupon Rate</th>
                <th className="num">YTM</th>
                <th className="num">Price</th>
              </tr>
            </thead>
            <tbody>
              {bonds.map((b) => (
                <tr key={b.id}>
                  <td>{b.name}</td>
                  <td className="num">{b.maturity_years}</td>
                  <td className="num">{pct(b.coupon_rate)}</td>
                  <td className="num">{pct(b.ytm)}</td>
                  <td className="num">
                    {priceError ? (
                      <span className="error">Error</span>
                    ) : prices[b.id] === undefined ? (
                      '…'
                    ) : (
                      num(prices[b.id])
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </section>
  )
}

export default BondTable
