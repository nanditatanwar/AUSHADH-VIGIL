from app.ml.model_loader import ModelStore
import time

ModelStore.load()

exp = ModelStore.explainer

print("Loaded")

# --------------------
print("Testing _find_row")
t = time.time()
row = exp._find_row("Ashwagandha", "Warfarin")
print("Done", time.time() - t)
print(type(row))

# --------------------
print("Testing _top_constituents")
t = time.time()
print(exp._top_constituents(row))
print("Done", time.time() - t)

# --------------------
print("Testing _kg_path")
t = time.time()
print(exp._kg_path(row))
print("Done", time.time() - t)