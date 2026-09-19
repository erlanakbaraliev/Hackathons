export const API_BASE = "http://localhost:8000";

async function request(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    let detail = res.statusText;
    try {
      detail = (await res.json()).detail ?? detail;
    } catch {
      /* ignore */
    }
    throw new Error(`${res.status}: ${detail}`);
  }
  return res.json();
}

export const getBonds = () => request("/bonds");
export const getBondPrice = (id) => request(`/bonds/${id}/price`);
export const getBondRisk = (id) => request(`/bonds/${id}/risk`);
export const getPortfolioRisk = (ids, weights) =>
  request(`/portfolio/risk?bond_ids=${ids.join(",")}&weights=${weights.join(",")}`);
