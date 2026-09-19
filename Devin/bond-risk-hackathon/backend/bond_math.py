from models import Bond


def cash_flows(bond: Bond) -> list[tuple[int, float]]:
    n = round(bond.maturity_years * bond.coupon_freq)
    c = bond.face_value * bond.coupon_rate / bond.coupon_freq
    flows = [(t, c) for t in range(1, n + 1)]
    flows[-1] = (n, c + bond.face_value)
    return flows


def price(bond: Bond) -> float:
    f = bond.coupon_freq
    y = bond.ytm
    return sum(cf / (1 + y / f) ** t for t, cf in cash_flows(bond))


def macaulay_duration(bond: Bond) -> float:
    f = bond.coupon_freq
    y = bond.ytm
    p = price(bond)
    return sum((t / f) * cf / (1 + y / f) ** t for t, cf in cash_flows(bond)) / p


def modified_duration(bond: Bond) -> float:
    return macaulay_duration(bond) / (1 + bond.ytm / bond.coupon_freq)


def convexity(bond: Bond) -> float:
    f = bond.coupon_freq
    y = bond.ytm
    p = price(bond)
    return sum(
        cf * t * (t + 1) / (1 + y / f) ** (t + 2) for t, cf in cash_flows(bond)
    ) / (p * f**2)


def risk_metrics(bond: Bond) -> dict:
    f = bond.coupon_freq
    y = bond.ytm
    flows = cash_flows(bond)
    p = 0.0
    mac_sum = 0.0
    conv_sum = 0.0
    for t, cf in flows:
        pv = cf / (1 + y / f) ** t
        p += pv
        mac_sum += (t / f) * pv
        conv_sum += cf * t * (t + 1) / (1 + y / f) ** (t + 2)
    macaulay = mac_sum / p
    return {
        "macaulay_duration": macaulay,
        "modified_duration": macaulay / (1 + y / f),
        "convexity": conv_sum / (p * f**2),
    }
