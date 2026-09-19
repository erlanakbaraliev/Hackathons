from pydantic import BaseModel


class Bond(BaseModel):
    id: int
    name: str
    face_value: float
    coupon_rate: float  # decimal, e.g. 0.05 = 5%
    coupon_freq: int  # payments per year
    maturity_years: float  # years from today
    ytm: float  # decimal, e.g. 0.045 = 4.5%
