import pandas as pd

df = pd.read_csv("data/raw/data.csv")
df.columns = [c.replace("\ufeff", "").strip() for c in df.columns]

r = lambda s: s.rank(pct=True)

# --- spend: category sum if present, else calibrated f5, else 0 ---
cat = df[["f6", "f7", "f8", "f9", "f10"]].sum(axis=1, min_count=1)
ratio = (cat[cat.notna()] / df.f5[cat.notna()]).median()   # ~12.5
spend = cat.fillna(df.f5 * ratio).fillna(0)

# --- fills where 0 is the economic truth (block-structured missingness) ---
f11 = df.f11.fillna(0)          # 0.5% missing, treat as good
pg = 1 - f11
f21 = df.f21.fillna(0)          # no rewards record -> no redemption cost
f17 = df.f17.fillna(0)          # no lend line -> no lend revenue
f1 = df.f1                      # no NaNs

# benefit-usage costs — 2.7% missing, shared segment, structural zero
f13 = df.f13.fillna(0)   # lounge access count
f14 = df.f14.fillna(0)   # airline credits used
f15 = df.f15.fillna(0)   # cab benefits usage
f16 = df.f16.fillna(df.f16.median())  # entertainment credit — has a floor ~8.88, not truly zero-missing

# risk/churn signals — 0% missing, no fill needed
f2 = df.f2   # cancellation calls
f3 = df.f3   # collection calls

f18 = df.f18.fillna(0)     # consumer lend line — 62% missing, same structural-zero logic as f17

f12 = df.f12.fillna(df.f12.median())   # logins
f19 = df.f19.fillna(df.f19.median())   # supp accounts
f20 = df.f20.fillna(df.f20.median())   # active cards



# cost of benefits actually paid out (what Amex spends, not what customer could use)
benefit_cost = 0.05*f13 + 0.4*f14 + 0.6*f15 + 0.3*f16

# distress/churn multiplier — a customer calling to cancel or being sent to collections
# is a near-term profitability drag independent of current balance/spend
distress = 1 - (0.25*f2 + 0.5*f3).clip(upper=1)

# --- five definitions, consensus of ranks (unchanged from 0.733) ---
# d1 = 0.02 * spend - 0.01 * f21
d1 = 0.02*spend - 0.01*f21 - benefit_cost
d2 = 0.22 * f1 * pg * distress - 0.7 * f1 * f11
d3 = 0.02 * spend + 0.22 * f1 * pg + 0.15 * (f17+f18) * pg - 0.01 * f21 - benefit_cost
d4 = spend
d5 = spend * pg
d6 = r(f12) + r(f19) + r(f20) - 2*r(f2) - 3*r(f3)

consensus = r(d1) + r(d2) + r(d3) + r(d4) + r(d5) + r(d6)
prediction = r(consensus) * 100

result = pd.DataFrame({"ID": df["id"], "Prediction": prediction.round(4)})

with pd.ExcelWriter("submission_1.xlsx", engine="openpyxl") as writer:
    result.to_excel(writer, sheet_name="Predictions", index=False)
    pd.DataFrame().to_excel(writer, sheet_name="Profitability Framework", index=False)

# raw = df.copy();
# check = result.merge(raw, left_on="ID", right_on="id")
# check['decile'] = pd.qcut(check['Prediction'], 10, labels=False, duplicates='drop')
# print(check.groupby('decile')[['f1','f5','f11','f2','f3','f17','f18','f21']].mean())

# formula_cols_df = pd.DataFrame({'d1':d1,'d2':d2,'d3':d3,'d4':d4,'d5':d5,'d6':d6})
# print(formula_cols_df.corr())