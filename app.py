"""LeadNormalizer - MVP de Normalizacion y Depuracion de Base de Prospeccion."""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from core.audit import build_audit_log, compute_kpis
from core.discard_rules import apply_discard_rules
from core.matcher import match_crm
from core.normalizer import normalize_data, normalize_headers
from core.report_generator import build_descartada_workbook, build_normalizada_workbook
from core.validator import ValidationError, validate_structure

BASE_DIR = Path(__file__).parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUTS_DIR = BASE_DIR / "outputs"

st.set_page_config(page_title="LeadNormalizer", layout="wide")


@st.cache_data
def load_config():
    headers_config = json.loads((CONFIG_DIR / "headers.json").read_text(encoding="utf-8"))
    rules_config = json.loads((CONFIG_DIR / "rules.json").read_text(encoding="utf-8"))
    return headers_config, rules_config


def procesar(df_crudo_raw: pd.DataFrame, df_crm_raw: pd.DataFrame, headers_config: dict, rules_config: dict):
    df, corrections_crudo = normalize_headers(df_crudo_raw, headers_config)
    crm_df, corrections_crm = normalize_headers(df_crm_raw, headers_config)

    validate_structure(df, rules_config["required_columns"])

    df = normalize_data(df)
    crm_df = normalize_data(crm_df)

    en_crm = match_crm(df, crm_df, rules_config["crm_match_keys"])
    df_validos, df_descartados = apply_discard_rules(df, en_crm, rules_config)

    kpis = compute_kpis(len(df_crudo_raw), df_validos, df_descartados)
    audit_df = build_audit_log(corrections_crudo, corrections_crm, kpis)

    return df_validos, df_descartados, kpis, audit_df, corrections_crudo, corrections_crm


def main():
    st.title("LeadNormalizer")
    st.caption("Normalizacion y depuracion de base de prospeccion vs. CRM")

    headers_config, rules_config = load_config()

    col1, col2 = st.columns(2)
    with col1:
        archivo_crudo = st.file_uploader("Base Prospeccion (Excel crudo)", type=["xlsx", "xls"])
    with col2:
        archivo_crm = st.file_uploader("Base CRM exportada (Excel)", type=["xlsx", "xls"])

    if not archivo_crudo or not archivo_crm:
        st.info("Carga ambos archivos para iniciar el procesamiento.")
        return

    df_crudo_raw = pd.read_excel(archivo_crudo, dtype=str)
    df_crm_raw = pd.read_excel(archivo_crm, dtype=str)

    if rules_config["crm_match_keys"][0] not in normalize_headers(df_crm_raw, headers_config)[0].columns:
        st.warning(
            "La base CRM no tiene una columna reconocible para "
            f"{rules_config['crm_match_keys'][0]}: no se detectaran DUPLICADO_CRM."
        )

    try:
        df_validos, df_descartados, kpis, audit_df, corr_crudo, corr_crm = procesar(
            df_crudo_raw, df_crm_raw, headers_config, rules_config
        )
    except ValidationError as error:
        st.error(str(error))
        return

    if corr_crudo or corr_crm:
        with st.expander("Correcciones de cabecera detectadas", expanded=True):
            if corr_crudo:
                st.write("Base Prospeccion:")
                st.table(pd.DataFrame(corr_crudo))
            if corr_crm:
                st.write("Base CRM:")
                st.table(pd.DataFrame(corr_crm))

    st.subheader("KPIs")
    kpi_cols = st.columns(len(kpis))
    for col, (nombre, valor) in zip(kpi_cols, kpis.items()):
        col.metric(nombre, valor)

    kpi_df = pd.DataFrame(
        {k: v for k, v in kpis.items() if k not in ("Registros Crudos", "Registros Validos", "Total Descartados")}.items(),
        columns=["Motivo", "Cantidad"],
    )

    graf_col1, graf_col2 = st.columns(2)
    with graf_col1:
        fig_barras = px.bar(kpi_df, x="Motivo", y="Cantidad", title="Descartes por motivo")
        st.plotly_chart(fig_barras, use_container_width=True)
    with graf_col2:
        if kpi_df["Cantidad"].sum() > 0:
            fig_torta = px.pie(kpi_df, names="Motivo", values="Cantidad", title="Distribucion de motivos de descarte")
            st.plotly_chart(fig_torta, use_container_width=True)
        else:
            st.info("No hubo registros descartados.")

    st.subheader("Descargas")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    normalizada_buffer = build_normalizada_workbook(df_validos, audit_df)
    descartada_buffer = build_descartada_workbook(df_descartados)

    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        st.download_button(
            "Descargar BaseProspeccionNormalizada.xlsx",
            data=normalizada_buffer,
            file_name=f"BaseProspeccionNormalizada_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    with dl_col2:
        st.download_button(
            "Descargar BaseProspeccionDescartada.xlsx",
            data=descartada_buffer,
            file_name=f"BaseProspeccionDescartada_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with st.expander("Ver registros validos"):
        st.dataframe(df_validos)
    with st.expander("Ver registros descartados"):
        st.dataframe(df_descartados)


if __name__ == "__main__":
    main()
