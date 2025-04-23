### 1. Créer un compte PythonAnywhere (PA)
- Free plan suffit (1 web app).

### 2. Charger le backend (API FastAPI)
1. Ouvrir un **bash console** sur PA.
2. `git clone` ou `scp` le dossier `backend/`.
3. `pip3 install --user -r backend/requirements.txt`
4. Dans l’onglet **Web** :
   - `Manual configuration` → *Python 3.10*.
   - Source code : répertoire `backend`.
   - WSGI file : remplacer le contenu par :
     ```python
     import sys, os
     from pathlib import Path
     from fastapi import FastAPI
     from mangum import Mangum  # si besoin
     path = Path(__file__).parent
     sys.path.append(str(path))
     from main import app as application  # noqa
     ```
   - **Reload**.

### 3. Streamlit sur PythonAnywhere
PA Free n’exécute pas de serveur long Streamlit. Deux options :
- **Solution simple** : exécuter Streamlit localement (VS Code) ; seuls les conseillers y ont accès via VPN.
- **Pro** (PA paid) : créer un second *always‑on task* qui lance `streamlit run frontend/app.py --server.port 8501` et configurer un proxy via le dashboard PA.