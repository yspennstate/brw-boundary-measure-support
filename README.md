# Support of the limiting boundary measure of branching random walk

Yitzchak Shmalo

This repository contains the paper and the computations for the following result. Let B be a supercritical branching random walk on a transient irreducible Markov chain, with an offspring law satisfying the L log L condition. Candellero and Hutchcroft (*On the boundary at infinity for branching random walk*, Electron. Commun. Probab. 28 (2023)) proved that m^{-n} B_n converges almost surely to a random measure W on the Martin boundary, and asked in their Problem 4.2 for conditions under which the support of W coincides almost surely with the set of accumulation points of B.

The paper shows that the two sets coincide almost surely whenever the boundary has a countable basis of open sets V such that the exit probability P_x(X_infinity in V) stays bounded away from zero as x tends to any point of V. This holds whenever the Martin compactification is Dirichlet regular, and so covers simple random walk on regular trees (with a self-contained proof) and finitely supported symmetric random walks on non-elementary hyperbolic groups, for every supercritical L log L offspring law, on both sides of the local survival threshold. The proof uses the expectation formula for W, the branching property and Levy's zero-one law, and needs no second moment.

## Contents

- `paper/main.tex`, `paper/main.pdf`: the paper.
- `code/tree_check.py`: exact rational check of the radial hitting probabilities on regular trees, a simulation check of P_x(hit a) = q^{-d(x,a)}, and twenty branching random walks on the 3-regular tree with the share of particles in each depth-two cone. Output in `code/tree_check_out.txt` and `code/tree_check.json`. Standard library only; runs in under a minute.
- `lean/MassPositivity.lean`: the algebraic step behind the one-particle lower bound, checked with Lean 4 and Mathlib.

## Running

    cd code
    python tree_check.py > tree_check_out.txt

The Lean file compiles inside any Lean 4 project with Mathlib (`lake env lean MassPositivity.lean`).

## License

Paper: CC BY 4.0. Code: MIT.
