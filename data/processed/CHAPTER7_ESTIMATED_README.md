# ⚠️ Chapter 7 (Housing Finance) — ESTIMATED, NOT OFFICIAL KNBS DATA

`chapter7_ESTIMATED_housing_finance.csv` is **not** part of the original Kenya
Housing Survey 2024 dataset. The Chapter 7 report (Housing Finance) was not
included in the source files this project was built from, so this file is a
**modeled estimate**, built from adjacent questions elsewhere in the survey that
touch on financing. **Do not present this as official KNBS Chapter 7 findings** —
anywhere this file's numbers are used (a chart, a report, a conversation with
colleagues), they need the same "estimated" label attached, not just here.

## What it's built from

| Component | Source table | What it measures |
|---|---|---|
| `formal_credit_use_pct` | Table 4.12 | Loan % + Mortgage % among modes of financing home acquisition (same denominator: all homeowners) |
| `institutional_channel_share_pct` | Table 4.13 | Share of financing that came through SACCOs + Commercial Banks + Housing Finance Institutions + Microfinance + Employer schemes, **among those who used some financing source** — a different, smaller denominator than the column above |
| `rent_to_expenditure_pct` | Table 4.2 | Rent as a share of household expenditure — context for financing pressure, not a finance-access measure itself |
| `awareness_composite_pct` | Tables 6.9, 6.12, 6.13 | Average of "aware of Affordable Housing Program," "aware of Affordable Housing Relief," and "aware of tax deductibility on housing loans" |
| `housing_finance_access_estimated_score_0_100` | Derived | Unweighted composite: (formal credit use + institutional channel share + awareness) − rent burden, min-max scaled 0–100 for ranking only |

## Known limitations — read before using this for anything

1. **Different denominators combined.** `formal_credit_use_pct` is a share of *all*
   homeowners; `institutional_channel_share_pct` is a share of only the (often very
   small) group who already used financing. Combining them into one score is a
   simplification, not a statistically rigorous index.
2. **Small base sizes in some counties.** Table 4.13's percentages are conditional on
   having used financing at all, and in several counties very few households did —
   a county showing 100% institutional share may reflect just one or two respondents,
   not a real pattern.
3. **44 of 47 counties only** — three counties were missing data in at least one of
   the six source tables and were excluded rather than filled in with a guess.
4. **No real credit-market data** (default rates, actual interest rates charged,
   mortgage-to-income ratios) exists anywhere in this dataset. This estimate can only
   speak to *how* people financed past acquisitions and *whether* they're aware of
   financing-related programs — not to loan affordability or credit risk.

## Recommended use

Fine for a portfolio project as a clearly-labeled "here's how I'd approach an
estimation problem when the real data isn't available" demonstration. **Not fine**
to present as, or let get mistaken for, actual KNBS Chapter 7 statistics. If the
real Chapter 7 report becomes available, replace this file and retire the estimate.
