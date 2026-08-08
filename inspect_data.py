from app.ml.model_loader import ModelStore

ModelStore.load()

exp = ModelStore.explainer

print("Rows:", len(exp.df))

print("Columns:")
print(exp.df.columns.tolist())

print("\nHerbs sample:")
print(exp.herbs_df.head())

print("\nDrugs sample:")
print(exp.drugs_df.head())