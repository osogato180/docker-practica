import os

import pandas as pd
import requests
import streamlit as st

API_URL = os.getenv("API_URL")

st.set_page_config(
    page_title="CRUD Demo",
    layout="wide"
)

st.title("🐳 Streamlit + FastAPI + PostgreSQL")

tab1 = st.tabs(["CRUD Productos"])[0]

with tab1:

    st.header("➕ Crear producto")

    with st.form("crear_producto"):

        nombre = st.text_input("Nombre")

        precio = st.number_input(
            "Precio",
            min_value=0.0
        )

        submitted = st.form_submit_button(
            "Guardar"
        )

        if submitted:

            response = requests.post(
                f"{API_URL}/productos",
                json={
                    "nombre": nombre,
                    "precio": precio
                }
            )

            if response.status_code == 200:
                st.success("Producto creado")

    st.divider()

    st.header("📋 Productos")

    response = requests.get(
        f"{API_URL}/productos"
    )

    productos = response.json()

    if productos:

        df = pd.DataFrame(productos)

        st.dataframe(
            df,
            use_container_width=True
        )

    st.divider()

    st.header("✏️ Actualizar")

    product_id = st.number_input(
        "ID producto",
        min_value=1,
        step=1
    )

    nuevo_nombre = st.text_input(
        "Nuevo nombre"
    )

    nuevo_precio = st.number_input(
        "Nuevo precio",
        min_value=0.0
    )

    if st.button("Actualizar"):

        requests.put(
            f"{API_URL}/productos/{product_id}",
            json={
                "nombre": nuevo_nombre,
                "precio": nuevo_precio
            }
        )

        st.success("Producto actualizado")

    st.divider()

    st.header("🗑️ Eliminar")

    delete_id = st.number_input(
        "ID eliminar",
        min_value=1,
        step=1
    )

    if st.button("Eliminar"):

        requests.delete(
            f"{API_URL}/productos/{delete_id}"
        )

        st.warning("Producto eliminado")
