from models import Bond

SEED_BONDS = [
    Bond(id=1,  name="US Treasury 2Y",   face_value=1000, coupon_rate=0.030, coupon_freq=2, maturity_years=2,  ytm=0.032),
    Bond(id=2,  name="US Treasury 5Y",   face_value=1000, coupon_rate=0.035, coupon_freq=2, maturity_years=5,  ytm=0.037),
    Bond(id=3,  name="US Treasury 10Y",  face_value=1000, coupon_rate=0.040, coupon_freq=2, maturity_years=10, ytm=0.042),
    Bond(id=4,  name="US Treasury 30Y",  face_value=1000, coupon_rate=0.045, coupon_freq=2, maturity_years=30, ytm=0.047),
    Bond(id=5,  name="Corp A 3Y",        face_value=1000, coupon_rate=0.038, coupon_freq=2, maturity_years=3,  ytm=0.041),
    Bond(id=6,  name="Corp A 7Y",        face_value=1000, coupon_rate=0.042, coupon_freq=2, maturity_years=7,  ytm=0.045),
    Bond(id=7,  name="Corp B 4Y",        face_value=1000, coupon_rate=0.050, coupon_freq=2, maturity_years=4,  ytm=0.048),
    Bond(id=8,  name="Corp B 12Y",       face_value=1000, coupon_rate=0.055, coupon_freq=2, maturity_years=12, ytm=0.053),
    Bond(id=9,  name="Muni 6Y",          face_value=1000, coupon_rate=0.028, coupon_freq=2, maturity_years=6,  ytm=0.030),
    Bond(id=10, name="Muni 15Y",         face_value=1000, coupon_rate=0.033, coupon_freq=2, maturity_years=15, ytm=0.035),
]
