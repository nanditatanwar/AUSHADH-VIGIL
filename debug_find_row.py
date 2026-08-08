from app.ml.model_loader import ModelStore
import pandas as pd
import time

ModelStore.load()
exp = ModelStore.explainer

print("Herb exists:", (exp.df["herb_name"] == "Ashwagandha").sum())
print("Drug exists:", (exp.df["drug_name"] == "Warfarin").sum())

print("Combined rows:")
print(
    exp.df[
        (exp.df["herb_name"] == "Ashwagandha") &
        (exp.df["drug_name"] == "Warfarin")
    ]
)

print("Now calling _find_row...")

t = time.time()
row = exp._find_row("Ashwagandha", "Warfarin")
print("Returned in", time.time() - t)
print(row)