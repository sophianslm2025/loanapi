# frontend/app.py
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:8000/predict"  # change après déploiement

st.set_page_config(page_title="Score d’éligibilité", layout="centered")
st.title("📊 Score d’éligibilité au prêt")

# --------- Fiche client / Saisie conseiller ------------------------
with st.form("form_features"):
    st.header("Caractéristiques du client")
    ext1 = st.slider("Score externe #1 (bureau A)", 0.0, 1.0, 0.45, 0.01)
    ext2 = st.slider("Score externe #2 (bureau B)", 0.0, 1.0, 0.34, 0.01)
    ext3 = st.slider("Score interne historique", 0.0, 1.0, 0.12, 0.01)
    age = st.slider("Âge (années)", 18, 85, 37)
    income = st.number_input("Revenu annuel (€)", 0, 1_000_000, 45_000, step=1_000)
    submitted = st.form_submit_button("Obtenir le score")

if submitted:
    payload = {
        "features": {
            "EXT_SOURCE_1": ext1,
            "EXT_SOURCE_2": ext2,
            "EXT_SOURCE_3": ext3,
            "DAYS_BIRTH": -age * 365,
            "AMT_INCOME_TOTAL": income,
        }
    }

    try:
        resp = requests.post(API_URL, json=payload, timeout=10)
        data = resp.json()
        resp.raise_for_status()

        score = data["score"] * 100  # en %
        expl = data.get("explanation", {})

        # ------------------ Jauge ------------------
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            gauge={"axis": {"range": [0, 100]}},
            number={"suffix": "%"},
            title={"text": "Probabilité d’acceptation"}
        ))
        st.plotly_chart(fig, use_container_width=True)

        # ------------------ Explications SHAP ------------------
        if expl:
            st.subheader("Principales contributions au score")
            df_exp = pd.DataFrame(
                [("Score externe #1", expl.get("EXT_SOURCE_1", 0)),
                 ("Score externe #2", expl.get("EXT_SOURCE_2", 0)),
                 ("Score interne",   expl.get("EXT_SOURCE_3", 0)),
                 ("Âge",              expl.get("DAYS_BIRTH", 0)),
                 ("Revenu annuel",    expl.get("AMT_INCOME_TOTAL", 0))],
                columns=["Facteur", "Impact"]
            )
            st.table(df_exp)
            # Phrase lisible
            best_feat, best_imp = max(expl.items(), key=lambda x: abs(x[1]))
            txt_map = {
                "EXT_SOURCE_1": "le Score externe #1",
                "EXT_SOURCE_2": "le Score externe #2",
                "EXT_SOURCE_3": "le Score interne historique",
                "DAYS_BIRTH": "l’âge du client",
                "AMT_INCOME_TOTAL": "le revenu annuel",
            }
            st.info(f"Le facteur le plus influent est **{txt_map[best_feat]}**.")
        else:
            st.warning("Aucune explication renvoyée par le modèle.")

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API : {e}")
    except ValueError:
        st.error("Réponse JSON inattendue.")