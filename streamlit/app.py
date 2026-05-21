import os
import pandas as pd
import requests
import streamlit as st

API_URL = os.getenv("API_URL")

st.set_page_config(
    page_title="HSR Damage Calculator",
    layout="wide"
)

st.title("⚔️ HSR Damage Calculator")

characters = [
    "Kafka",
    "Jingliu",
    "Acheron",
    "Firefly",
    "Blade",
    "Dan Heng IL"
]

st.header("📊 Calcular daño")

with st.form("damage_form"):

    personaje = st.selectbox(
        "Personaje",
        characters
    )

    atk = st.number_input(
        "ATK",
        min_value=0,
        value=2500
    )

    crit_rate = st.slider(
        "Crit Rate %",
        0,
        100,
        70
    )

    crit_dmg = st.slider(
        "Crit DMG %",
        0,
        400,
        150
    )

    bonus = st.slider(
        "Bonus Damage %",
        0,
        200,
        50
    )

    multiplicador = st.number_input(
        "Skill Multiplier %",
        min_value=0,
        value=240
    )

    submitted = st.form_submit_button(
        "Calcular"
    )

    if submitted:

        payload = {
            "personaje": personaje,
            "atk": atk,
            "crit_rate": crit_rate,
            "crit_dmg": crit_dmg,
            "bonus": bonus,
            "multiplicador": multiplicador
        }

        response = requests.post(
            f"{API_URL}/calcular",
            json=payload
        )

        data = response.json()

        st.success(
            f"🔥 Daño Final: {data['daño_final']}"
        )

st.divider()

st.header("💾 Historial de builds")

response = requests.get(
    f"{API_URL}/builds"
)

builds = response.json()

if builds:

    df = pd.DataFrame(builds)

    st.dataframe(
        df,
        use_container_width=True
    )