# backend/train_pipeline.py
import pandas as pd
import joblib
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
import sklearn
from packaging import version

# ------------------------------------------------------------------
# 1) Charger les données
# ------------------------------------------------------------------
df = pd.read_csv("../data/application_train.csv")      # adapte le chemin si besoin

# ------------------------------------------------------------------
# 2) Choisir features + cible
# ------------------------------------------------------------------
FEATURES = [
    "EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3",
    "DAYS_BIRTH", "AMT_INCOME_TOTAL"
]
TARGET = "TARGET"

X = df[FEATURES]
y = df[TARGET]

# ------------------------------------------------------------------
# 3) Pré-processing
# ------------------------------------------------------------------
num_feats = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_feats = X.select_dtypes(include=["object"]).columns.tolist()

num_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Choix du paramètre 'sparse' / 'sparse_output' suivant la version de scikit-learn
skl_ver = sklearn.__version__
if version.parse(skl_ver) >= version.parse("1.2"):
    ohe_params = {"handle_unknown": "ignore", "sparse_output": False}
else:
    ohe_params = {"handle_unknown": "ignore", "sparse": False}

cat_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value="NA")),
    ("ohe", OneHotEncoder(**ohe_params))
])

preproc = ColumnTransformer([
    ("num", num_pipe, num_feats),
    ("cat", cat_pipe, cat_feats)
])

# ------------------------------------------------------------------
# 4) Pipeline complet
# ------------------------------------------------------------------
pipe = Pipeline([
    ("preproc", preproc),
    ("clf", GradientBoostingClassifier(n_estimators=100, random_state=42))
])

# ------------------------------------------------------------------
# 5) Entraînement
# ------------------------------------------------------------------
print("▶️  Entraînement du pipeline…")
pipe.fit(X, y)
print("✅  Entraînement terminé.")

# ------------------------------------------------------------------
# 6) Export du pipeline
# ------------------------------------------------------------------
out_folder = Path(__file__).parent / "model"
out_folder.mkdir(parents=True, exist_ok=True)
out_path = out_folder / "pipeline.pkl"
joblib.dump(pipe, out_path)
print(f"✅  pipeline.pkl exporté dans {out_path}")