import pytest
from fastapi.testclient import TestClient

import bond_math
from data import SEED_BONDS
from main import app
from models import Bond

client = TestClient(app)


def make_bond(**overrides) -> Bond:
    params = dict(
        id=0,
        name="test",
        face_value=1000,
        coupon_rate=0.05,
        coupon_freq=2,
        maturity_years=2,
        ytm=0.05,
    )
    params.update(overrides)
    return Bond(**params)


def test_par_bond_price():
    b = make_bond()
    assert abs(bond_math.price(b) - 1000) < 0.5


def test_par_bond_durations():
    b = make_bond()
    mac = bond_math.macaulay_duration(b)
    assert 0 < mac < 2
    assert bond_math.modified_duration(b) == pytest.approx(mac / 1.025)


def test_convexity_positive():
    b = make_bond()
    assert bond_math.convexity(b) > 0


def test_premium_bond():
    b = make_bond(coupon_rate=0.06, ytm=0.04)
    assert bond_math.price(b) > 1000


def test_discount_bond():
    b = make_bond(coupon_rate=0.03, ytm=0.05)
    assert bond_math.price(b) < 1000


def test_zero_coupon_bond():
    b = make_bond(coupon_rate=0, maturity_years=5, ytm=0.04)
    assert bond_math.macaulay_duration(b) == pytest.approx(5.0)
    assert bond_math.price(b) == pytest.approx(1000 / 1.02**10)


def test_list_bonds():
    r = client.get("/bonds")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 10
    assert [b["id"] for b in body] == list(range(1, 11))


def test_get_price():
    r = client.get("/bonds/1/price")
    assert r.status_code == 200
    assert r.json() == {"bond_id": 1, "price": round(bond_math.price(SEED_BONDS[0]), 4)}


def test_get_price_not_found():
    r = client.get("/bonds/999/price")
    assert r.status_code == 404
    assert "detail" in r.json()


def test_get_risk():
    r = client.get("/bonds/1/risk")
    assert r.status_code == 200
    body = r.json()
    assert set(body) == {"bond_id", "macaulay_duration", "modified_duration", "convexity"}
    assert body["macaulay_duration"] == round(bond_math.macaulay_duration(SEED_BONDS[0]), 4)


def test_get_risk_not_found():
    r = client.get("/bonds/999/risk")
    assert r.status_code == 404
    assert "detail" in r.json()


def test_portfolio_risk():
    r = client.get("/portfolio/risk?bond_ids=1,2&weights=0.5,0.5")
    assert r.status_code == 200
    md1 = bond_math.modified_duration(SEED_BONDS[0])
    md2 = bond_math.modified_duration(SEED_BONDS[1])
    assert r.json()["portfolio_duration"] == pytest.approx(0.5 * md1 + 0.5 * md2, abs=1e-3)


@pytest.mark.parametrize(
    "query",
    [
        "bond_ids=1,2&weights=0.5",
        "bond_ids=1,2&weights=0.5,0.3",
        "bond_ids=1,999&weights=0.5,0.5",
        "bond_ids=a,b&weights=0.5,0.5",
    ],
)
def test_portfolio_risk_400(query):
    r = client.get(f"/portfolio/risk?{query}")
    assert r.status_code == 400
    assert "detail" in r.json()
