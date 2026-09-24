# Index Integrity: Deflation, Substitution Bias & Goodhart's Law

## Objective
Audit how economic and business metrics can mislead, by debugging a price deflation pipeline, measuring substitution bias in the CPI, and detecting metric gaming in a KPI dashboard.

## Methodology
- Diagnosed and fixed four bugs in a deflation function using FRED data (AHETPI wages, CPIAUCSL): a single-month base period, misaligned dates, unhandled missing values, and output in 1982-84 dollars mislabelled as 2020 dollars.
- Compared CPI-U (CPIAUCNS) with Chained CPI (C-CPI-U) from December 1999, converting the gap from index points into annual inflation rates using compound growth.
- Built a two-panel KPI dashboard tracking DAU/MAU against time per session, and measured the correlation between them before and after a simulated gaming period.
- Packaged the corrected function as a tested Python module, `deflation_utils.py`.
- Built an interactive monitor with ipywidgets and plotly to recompute the substitution gap and flag when the KPI correlation turns negative.

## Key Findings
- The corrected pipeline gives a real wage of $24.43 in January 1973 (2020 dollars), with the series peaking at $25.42 in April 2020, a composition effect rather than a raise.
- CPI-U rose 2.61% a year versus 2.35% for C-CPI-U, an upper-level substitution bias of 0.27 pp per year, above the Boskin Commission's 0.15 pp estimate. The 0.50 index points per year gap is not a rate and should not be compared with it.
- The correlation between DAU/MAU and time per session flipped from +0.93 to -0.96 once gaming began, a clear signal of Goodhart's Law.
