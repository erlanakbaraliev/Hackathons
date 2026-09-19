from fastapi import APIRouter, HTTPException, Query

import bond_math
import data
from models import PortfolioRiskResponse

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/risk", response_model=PortfolioRiskResponse)
def portfolio_risk(
    bond_ids: str = Query(...),
    weights: str = Query(...),
):
    try:
        ids = [int(x) for x in bond_ids.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="bond_ids must be comma-separated integers")
    try:
        ws = [float(x) for x in weights.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="weights must be comma-separated numbers")
    if not ids or not ws:
        raise HTTPException(status_code=400, detail="bond_ids and weights must be non-empty")
    if len(ids) != len(ws):
        raise HTTPException(
            status_code=400,
            detail=f"bond_ids ({len(ids)}) and weights ({len(ws)}) must have the same length",
        )
    if abs(sum(ws) - 1.0) > 0.01:
        raise HTTPException(status_code=400, detail=f"weights must sum to 1.0 (got {sum(ws)})")
    bonds_by_id = {b.id: b for b in data.SEED_BONDS}
    for bid in ids:
        if bid not in bonds_by_id:
            raise HTTPException(status_code=400, detail=f"Unknown bond id {bid}")
    duration = 0.0
    convexity = 0.0
    for bid, w in zip(ids, ws):
        metrics = bond_math.risk_metrics(bonds_by_id[bid])
        duration += w * metrics["modified_duration"]
        convexity += w * metrics["convexity"]
    return PortfolioRiskResponse(
        portfolio_duration=round(duration, 4),
        portfolio_convexity=round(convexity, 4),
    )
