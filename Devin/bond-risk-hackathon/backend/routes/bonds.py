from fastapi import APIRouter, HTTPException

import bond_math
import data
from models import Bond, PriceResponse, RiskResponse

router = APIRouter(prefix="/bonds", tags=["bonds"])


def get_bond_or_404(bond_id: int) -> Bond:
    for bond in data.SEED_BONDS:
        if bond.id == bond_id:
            return bond
    raise HTTPException(status_code=404, detail=f"Bond {bond_id} not found")


@router.get("", response_model=list[Bond])
def list_bonds():
    return data.SEED_BONDS


@router.get("/{bond_id}/price", response_model=PriceResponse)
def get_price(bond_id: int):
    bond = get_bond_or_404(bond_id)
    return PriceResponse(bond_id=bond.id, price=round(bond_math.price(bond), 4))


@router.get("/{bond_id}/risk", response_model=RiskResponse)
def get_risk(bond_id: int):
    bond = get_bond_or_404(bond_id)
    metrics = bond_math.risk_metrics(bond)
    return RiskResponse(
        bond_id=bond.id,
        macaulay_duration=round(metrics["macaulay_duration"], 4),
        modified_duration=round(metrics["modified_duration"], 4),
        convexity=round(metrics["convexity"], 4),
    )
