"""
Relativistic rocket with constant proper acceleration and a flip-and-burn
at the midpoint. One-way and round-trip figures for spot-checking.

Frame conventions
-----------------
- a   : proper acceleration (felt aboard ship), constant in magnitude.
- D   : one-way distance in the Earth (rest) frame.
- T_e : coordinate time elapsed in Earth frame.
- tau : proper time elapsed aboard ship.
- All quantities below assume the ship starts and ends at rest relative to
  Earth (i.e. accelerate for D/2, flip, decelerate for D/2).

Closed-form equations
---------------------
For motion starting from rest under constant proper acceleration a,
covering a rest-frame distance x:

    T_e(x)   = sqrt( (x/c)^2  + 2 x / a )
    tau(x)   = (c / a) * acosh( 1 + a x / c^2 )
    gamma(x) = 1 + a x / c^2            (Lorentz factor reached at distance x)
    v(x)/c   = sqrt(1 - 1/gamma^2)

For a flip-at-midpoint trip of total one-way distance D, by symmetry
each leg covers D/2, so:

    T_e_oneway  = 2 * T_e(D/2)
    tau_oneway  = 2 * tau(D/2)
    gamma_peak  = 1 + a (D/2) / c^2     (at the flip point)

Round trip just doubles both totals (four equal accel/decel phases).

Sanity checks built in:
- Non-relativistic limit  a*T << c   =>  T_e ~ tau ~ 2*sqrt(D/a).
- Ultra-relativistic limit a*D >> c^2 =>  tau ~ (2c/a) * ln(a D / c^2).
"""

from math import sqrt, acosh, log, cosh

# --- constants (SI) ---
c        = 299_792_458.0           # m/s
g0       = 9.806_65                # m/s^2  (standard gravity)
ly       = 9.460_730_472_580_8e15  # m      (IAU light year)
year_s   = 365.25 * 86400.0        # s      (Julian year, matches the ly defn)


def leg(a, x):
    """Single accel-from-rest leg covering rest-frame distance x.

    Returns dict with Earth time, proper time, Lorentz factor and velocity
    fraction reached at the end of the leg.
    """
    T_e   = sqrt((x / c) ** 2 + 2.0 * x / a)
    tau   = (c / a) * acosh(1.0 + a * x / c ** 2)
    gamma = 1.0 + a * x / c ** 2
    beta  = sqrt(1.0 - 1.0 / gamma ** 2)
    return dict(T_e=T_e, tau=tau, gamma=gamma, beta=beta)


def flip_trip(a_g, D_ly):
    """Flip-and-burn one-way trip at proper accel a_g (in g) over D_ly ly."""
    a = a_g * g0
    D = D_ly * ly
    half = leg(a, D / 2.0)
    T_e_one = 2.0 * half["T_e"]
    tau_one = 2.0 * half["tau"]
    return dict(
        a_g         = a_g,
        a_si        = a,
        D_ly        = D_ly,
        D_m         = D,
        gamma_peak  = half["gamma"],
        beta_peak   = half["beta"],
        T_e_oneway  = T_e_one,
        tau_oneway  = tau_one,
        T_e_round   = 2.0 * T_e_one,
        tau_round   = 2.0 * tau_one,
        dilation    = T_e_one / tau_one,  # average dilation over the trip
    )


def fmt_years(s):
    return f"{s / year_s:.4f} yr"


def report(r):
    print(f"  proper acceleration : {r['a_g']:.3f} g  ({r['a_si']:.4f} m/s^2)")
    print(f"  one-way distance    : {r['D_ly']:.4f} ly")
    print(f"  peak Lorentz factor : {r['gamma_peak']:.4f}")
    print(f"  peak velocity       : {r['beta_peak']:.6f} c")
    print(f"  one-way Earth time  : {fmt_years(r['T_e_oneway'])}")
    print(f"  one-way ship time   : {fmt_years(r['tau_oneway'])}")
    print(f"  round-trip Earth    : {fmt_years(r['T_e_round'])}")
    print(f"  round-trip ship     : {fmt_years(r['tau_round'])}")
    print(f"  avg time dilation   : {r['dilation']:.4f}x  (Earth yr per ship yr)")


def sanity_checks():
    print("\n[sanity] non-relativistic limit (a=1e-6 g, D=1e-6 ly)")
    a = 1e-6 * g0
    x = 1e-6 * ly
    nr_T  = 2.0 * sqrt(x / a)            # classical 2*sqrt(d/a) for accel+decel? no, one leg
    leg1  = leg(a, x)
    # one leg classical: T = sqrt(2 x / a)
    classical = sqrt(2.0 * x / a)
    print(f"    relativistic leg T_e = {leg1['T_e']:.6e} s")
    print(f"    classical  sqrt(2x/a) = {classical:.6e} s")
    print(f"    ratio                 = {leg1['T_e']/classical:.8f}  (expect 1.0)")
    print(f"    tau/T_e               = {leg1['tau']/leg1['T_e']:.8f}  (expect 1.0)")

    print("\n[sanity] ultra-relativistic limit (a=1 g, D=1e6 ly)")
    a = 1.0 * g0
    x = 1e6 * ly / 2.0
    L = leg(a, x)
    approx_tau = (c / a) * log(2.0 * a * x / c ** 2)
    print(f"    exact   tau = {L['tau']:.6e} s")
    print(f"    approx  tau = {approx_tau:.6e} s  ((c/a) ln(2 a x / c^2))")
    print(f"    ratio       = {L['tau']/approx_tau:.6f}  (expect ~1.0)")


if __name__ == "__main__":
    print("Tau Ceti @ 1.5 g, flip-and-burn (D = 11.9 ly)")
    print("-" * 56)
    report(flip_trip(a_g=1.5, D_ly=11.9))

    print("\nReference cases for cross-checking")
    print("-" * 56)
    print("\nProxima Centauri @ 1.0 g (D = 4.246 ly)")
    report(flip_trip(a_g=1.0, D_ly=4.246))
    print("\nTau Ceti @ 1.0 g  (D = 11.9 ly)")
    report(flip_trip(a_g=1.0, D_ly=11.9))
    print("\nAndromeda @ 1.0 g (D = 2.537e6 ly)  -- the famous one")
    report(flip_trip(a_g=1.0, D_ly=2.537e6))

    sanity_checks()
