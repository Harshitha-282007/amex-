import pandas as pd

df = pd.read_csv("data/raw/data.csv")
df.columns = [c.replace("\ufeff", "").strip() for c in df.columns]


d0 = df.fillna(0)
r  = lambda s: s.rank(pct=True)

pg = (1 - d0.f11) ** 1.5                      # try nonlinear risk decay
distress = 1 - (0.5*d0.f2 + 0.5*d0.f3).clip(0, 1)
health = pg * distress                         # combined risk+distress factor

other  = d0.f7 + d0.f8 + d0.f10
travel = d0.f6 + d0.f9
margin = 0.054*other + 0.016*travel

interest  = 0.24*d0.f1*health - 0.9*d0.f1*d0.f11
lend      = 0.06*d0.f17*health
benefit   = 50*d0.f13 + d0.f14 + 15*d0.f15 + d0.f16
liability = 0.005*d0.f4                        # unrealized rewards cost

d1 = margin - 0.01*d0.f21 - benefit - liability
d2 = interest
d3 = margin + interest + lend - 0.01*d0.f21 - benefit - liability
d4 = margin
d5 = margin * health
d6 = d3 * (0.5 + 0.5*r(d0.f12 + d0.f19 + d0.f20))   # tenure/engagement-adjusted P&L

consensus  = r(d1) + r(d2) + r(d3) + r(d4) + r(d5) + r(d6)
prediction = (r(consensus) * 100).round(4)



result = pd.DataFrame({"ID": df["id"], "Prediction": prediction.round(4)})

with pd.ExcelWriter("submission_2.xlsx", engine="openpyxl") as writer:
    result.to_excel(writer, sheet_name="Predictions", index=False)
    pd.DataFrame().to_excel(writer, sheet_name="Profitability Framework", index=False)
