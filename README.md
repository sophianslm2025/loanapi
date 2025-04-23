# Loan‑Dashboard – Guide complet

Ce dépôt regroupe :
- **backend/** : API FastAPI (prédiction + explications)
- **frontend/** : Dashboard Streamlit pour les conseillers
- **data/** : (optionnel) jeux de données Kaggle si tu veux ré‑entraîner le modèle
- **backend/model/** : pipeline entraîné (`pipeline.pkl`)

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
$ git clone https://github.com/ton_user/loan_dashboard.git
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
## 6. Déploiement (gratuit)

### 6.1 API FastAPI sur PythonAnywhere **Free** (pas de carte bleue)

| Étape | Commande / Action |
|-------|-------------------|
| **a.** Crée un compte | <https://www.pythonanywhere.com> → **Register** (plan Free) |
| **b.** Ouvre une *Bash console* | Dashboard ▸ **Open bash** |
| **c.** Clone ou upload le dépôt | `git clone https://github.com/<toi>/loan_dashboard.git`  
*(ou `scp`/ZIP)* |
| **d.** Crée + active un venv | `python3.11 -m venv venv && source venv/bin/activate` |
| **e.** Installe les libs | `pip install --no-cache-dir -r loan_dashboard/backend/requirements.txt mangum` |
| **f.** New Web App | Dashboard ▸ **Web** ▸ *Add a new web app* ▸ **Manual configuration** ▸ Python 3.11 |
| **g.** Répertoire source | `/home/<user>/loan_dashboard/backend` |
| **h.** Virtualenv | `/home/<user>/venv` (sélecteur PA) |
| **i.** Fichier WSGI | *Clique* « WSGI file » et colle :  |

```python
import sys, os
from pathlib import Path
path = Path.home() / 'loan_dashboard' / 'backend'
sys.path.append(str(path))
from mangum import Mangum               # déjà installé à l’étape e
from main import app as fastapi_app
application = Mangum(fastapi_app)
```
| **j.** Reload l’app | bouton **Reload** sur la page Web |
| **k.** Tester | <https://<user>.pythonanywhere.com/docs> (Swagger) |

### 6.2 Dashboard Streamlit (100 % gratuit en **local**)

Le plan gratuit PA ne permet **pas** d’héberger Streamlit :
> Lance la commande suivante sur les postes conseillers (ou un serveur interne) :

```bash
cd loan_dashboard/frontend
streamlit run app.py
```

- L’URL de l’API dans `app.py` doit pointer :
  ```python
  API_URL = "https://<user>.pythonanywhere.com/predict"
  ```
- Accès au dashboard : `http://localhost:8501` (ou IP du serveur interne).

### 6.3 (Option payant) – Streamlit Community Cloud / PA Hacker
Si tu souhaites un hébergement public :
1. Crée un repo GitHub avec `frontend/app.py` et `requirements.txt`.
2. <https://share.streamlit.io> ▸ **New app** ; mets `API_URL` dans les *secrets* :
   ```toml
   API_URL = "https://<user>.pythonanywhere.com/predict"
   ```
3. L’app est disponible sur `https://<ton-slug>.streamlit.app`.

---

