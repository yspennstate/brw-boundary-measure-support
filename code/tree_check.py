"""Checks for the regular-tree example.

1. Exact rational check of the radial hitting probabilities on the (q+1)-regular tree:
   f_L(r) = (q^-r - q^-L) / (1 - q^-L) satisfies f_L(0)=1, f_L(L)=0 and
   (q+1) f_L(r) = f_L(r-1) + q f_L(r+1) for 0<r<L, for q=2..8 and L=2..30.
2. Monte Carlo of P_x(hit a) = q^-d(x,a) for the radial chain (q=2,3, d=1..4).
3. Branching random walk on the 3-regular tree (q=2) with binary branching: the share of
   generation-n particles in each of the six depth-2 cones, over independent runs. Under the
   theorem the limiting measure charges every cone, and each cone has expected share 1/6.
Standard library only. Output: tree_check_out.txt (stdout) and tree_check.json.
"""
import json, random, pathlib
from fractions import Fraction as F

out = {}

# 1. exact recurrence
n_checks = 0
for q in range(2, 9):
    for L in range(2, 31):
        f = lambda r: (F(1, q**r) - F(1, q**L)) / (1 - F(1, q**L))
        assert f(0) == 1 and f(L) == 0
        n_checks += 2
        for r in range(1, L):
            assert (q + 1) * f(r) == f(r - 1) + q * f(r + 1)
            n_checks += 1
print(f"1. exact radial recurrence: {n_checks} identities checked, q=2..8, L=2..30, all hold")
out["exact_checks"] = n_checks

# 2. hitting probabilities by simulation of the distance chain
rng = random.Random(20261105)
rows = []
for q in (2, 3):
    for d in range(1, 5):
        trials, hits = 40000, 0
        for _ in range(trials):
            r = d
            while 0 < r < 60:
                r += -1 if rng.random() < 1 / (q + 1) else 1
            hits += r == 0
        p = hits / trials
        se = (p * (1 - p) / trials) ** 0.5
        z = (p - q**-d) / se
        rows.append(dict(q=q, d=d, simulated=p, exact=q**-d, z=z))
        print(f"2. q={q} d={d}  simulated {p:.4f}  exact {q**-d:.4f}  z {z:+.2f}")
out["hitting"] = rows


# 3. BRW on the 3-regular tree; a vertex is the reduced word from the root, letters 0..2 at
#    the first step and 0..1 afterwards (the child index among the q forward neighbours).
def step(v):
    k = len(v)
    nbrs = 3  # degree q+1 = 3
    i = rng.randrange(nbrs)
    if k == 0:
        return (i,)
    if i == 0:
        return v[:-1]
    return v + (i - 1,)


cone_rows = []
for run in range(20):
    gen = [()]
    for n in range(17):
        nxt = []
        for v in gen:
            nxt.append(step(v))
            nxt.append(step(v))
        gen = nxt
    counts = {}
    inside = 0
    for v in gen:
        if len(v) >= 2:
            counts[v[:2]] = counts.get(v[:2], 0) + 1
            inside += 1
    shares = [counts.get((a, b), 0) / len(gen) for a in range(3) for b in range(2)]
    cone_rows.append(dict(run=run, particles=len(gen), shares=shares,
                          share_at_depth_below_2=1 - inside / len(gen)))
mins = [min(r["shares"]) for r in cone_rows]
print(f"3. BRW, q=2, binary branching, generation 17 ({cone_rows[0]['particles']} particles), 20 runs")
print(f"   smallest depth-2 cone share in each run: min {min(mins):.4f}, median {sorted(mins)[10]:.4f}")
allshares = [s for r in cone_rows for s in r["shares"]]
print(f"   mean cone share over runs and cones {sum(allshares)/len(allshares):.4f} (expected 1/6 = 0.1667, less the mass still within depth 1)")
out["brw_cones"] = cone_rows
pathlib.Path(__file__).with_name("tree_check.json").write_text(json.dumps(out, indent=1))
