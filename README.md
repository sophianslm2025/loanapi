# Loan‑Dashboard – Guide complet

Ce dépôt regroupe :
- **backend/** : API FastAPI (prédiction + explications)
- **frontend/** : Dashboard Streamlit pour les conseillers
- **data/** : (optionnel) jeux de données Kaggle si tu veux ré‑entraîner le modèle
- **model/** : pipeline entraîné (`pipeline.pkl`)

> 🖥️ **Objectif** : lancer l’API et le dashboard **en local** _ou_ les déployer gratuitement (PythonAnywhere + Streamlit Cloud).

---
## 1. Arborescence
```
loan_dashboard/
├─ backend/
│  ├─ main.py                # FastAPI routes
│  ├─ serve_model.py         # utils (load, predict, SHAP)
│  ├─ train_pipeline.py      # script d’entraînement
│  ├─ requirements.txt       # dépendances API + ML
│  └─ model/pipeline.pkl     # pipeline entraîné
├─ frontend/
│  ├─ app.py                 # Streamlit app
│  └─ requirements.txt       # streamlit, requests, pandas, plotly
└─ data/ (optionnel)
```

---
## 2. Prérequis
- **Python 3.8+** (idéal 3.10/3.11).  
- Git (facultatif pour cloner).  
- Option : compte **PythonAnywhere** (plan Free) + compte **Streamlit Cloud**.

---
## 3. Installation **en local**
```bash
# Clone du repo
$ git clone https://github.com/sophianslm2025/loanapi.git
$ cd loan_dashboard

# Création + activation d’un venv
$ python -m venv venv
# Windows
$ venv\Scripts\activate
# macOS/Linux
$ source venv/bin/activate

# Dépendances backend + frontend
(venv) $ pip install -r backend/requirements.txt
(venv) $ pip install -r frontend/requirements.txt
```

### 3.1 (Optionnel) Ré‑entraîner le pipeline
Si tu veux régénérer `pipeline.pkl` :
- Télécharger le csv application_train.csv et le mettre dans le dossier ./data depuis -> https://www.kaggle.com/code/moizzz/applied-predictive-modelling-brief-overview
```bash
(venv) $ cd backend
(venv) $ python train_pipeline.py   # lit data/application_train.csv
```
Le fichier `backend/model/pipeline.pkl` est mis à jour.

---
## 4. Lancer **l’API** FastAPI (local)
```bash
(venv) $ cd backend
(venv) $ uvicorn main:app --reload
```
- Swagger : <http://127.0.0.1:8000/docs>
- Exemple requête :
  ```bash
  curl -X POST http://127.0.0.1:8000/predict \
    -H "Content-Type: application/json" \
    -d '{"features":{"EXT_SOURCE_1":0.6,"EXT_SOURCE_2":0.5,"EXT_SOURCE_3":0.4,"DAYS_BIRTH":-12000,"AMT_INCOME_TOTAL":45000}}'
  ```

---
## 5. Lancer **le dashboard Streamlit** (local)
```bash
(venv) $ cd frontend
(venv) $ streamlit run app.py
```
- Dashboard : <http://localhost:8501>
- Remplis le formulaire, clique **Obtenir le score**.

> **Astuce** : l’URL de l’API est paramétrée en haut de `frontend/app.py` (`API_URL`). Pour un usage local, laisse `http://127.0.0.1:8000/predict`.

---
## 6. Déploiement **gratuit**

### 6.1 API sur PythonAnywhere Free
1. Upload du dossier `backend/` sur PA via Git ou ZIP.  
2. Crée un venv, installe `pip install -r backend/requirements.txt mangum`.  
3. Configure la Web app : chemin source = `~/loan_dashboard/backend`, fichier WSGI :
   ```python
   import sys, os
   from pathlib import Path
   path = Path.home() / 'loan_dashboard' / 'backend'
   sys.path.append(str(path))
   from mangum import Mangum
   from main import app as fastapi_app
   application = Mangum(fastapi_app)
   ```
4. **Reload** → API accessible sur `https://<username>.pythonanywhere.com/predict`.

### 6.2 Dashboard sur Streamlit Community Cloud
1. Crée un repo GitHub avec `frontend/app.py` + `frontend/requirements.txt`.  
2. <https://share.streamlit.io> → **New app** → choisis le repo + `app.py`.  
3. Dans *Advanced ▸ Secrets* :
   ```toml
   API_URL = "https://<username>.pythonanywhere.com/predict"
   ```
4. Dans `app.py` :
   ```python
   import streamlit as st
   API_URL = st.secrets["API_URL"]
   ```
5. **Deploy** → URL `https://<user>-loan-dashboard.streamlit.app`.

---
## 7. Structure RGPD & Sécurité
| Point | Mise en œuvre |
|-------|---------------|
| Minimisation | 5 variables pseudonymisées envoyées à l’API |
| Pseudonymisation | ID client en UUID non exposé publiquement |
| Chiffrement | TLS via HTTPS PythonAnywhere & Streamlit Cloud |
| Droits | Endpoints à ajouter : GET/DELETE `/client/{id}` |
| Logs | Rotation 30 jours, IP tronquées, pas de payload complet |

---
## 8. FAQ rapide
- **Erreur 400 “KeyError 'EXT_SOURCE_1'”** : vérifie que le JSON contient bien les 5 features exactes.
- **SHAP explanation vide** : assure‑toi que `serve_model.py` utilise `TreeExplainer` et que `pipeline.pkl` est chargé.
- **Streamlit Cloud timeout** : l’app se met en veille au bout d’1h d’inactivité ; elle se réveille en 10 s.

---
### Made with ❤️ by Sophian — Dernière mise à jour : avril 2025

