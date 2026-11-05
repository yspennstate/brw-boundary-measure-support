import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Data.Real.Basic

-- Deterministic algebra in step 2; e is E W(V), t is the tail bound.
theorem mass_positive_lower_bound (c k p e t : Real)
    (hc : 0 < c) (hk : 0 < k) (he : c <= e)
    (hupper : e <= k * p + t) (ht : t <= c / 2) :
    c / (2 * k) <= p := by
  apply (div_le_iff₀ (by positivity : 0 < 2 * k)).2
  nlinarith

theorem positive_success_probability (c k p e t : Real)
    (hc : 0 < c) (hk : 0 < k) (he : c <= e)
    (hupper : e <= k * p + t) (ht : t <= c / 2) : 0 < p := by
  have h := mass_positive_lower_bound c k p e t hc hk he hupper ht
  have hpos : 0 < c / (2 * k) := by positivity
  linarith
