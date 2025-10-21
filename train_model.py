import pandas as pd
from catboost import CatBoostClassifier, Pool

df = pd.read_csv("dataset.csv")

# ---------- Preprocess ----------
categorical_cols = ['product','animal','time_of_day','storage','size','condition','type','name','ripeness']
for col in categorical_cols:
    df[col] = df[col].fillna('unknown').astype(str)

numeric_cols = ['days_since','density','fat','snf','purity','moisture','quantity','freshness']
for col in numeric_cols:
    df[col] = df[col].fillna(0)

X = df.drop(columns=['grade'])
y = df['grade']

# ---------- Train CatBoost ----------
model = CatBoostClassifier(iterations=3000, depth=6, learning_rate=0.1, verbose=100)
train_pool = Pool(X, y, cat_features=categorical_cols)
model.fit(train_pool)

# Save model
model.save_model("quality_grade_model.cbm")
print("Model trained and saved.")
