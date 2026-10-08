"""KPIs y log de auditoria (correcciones de cabeceras aplicadas)."""

import pandas as pd


def compute_kpis(total_crudos: int, df_validos: pd.DataFrame, df_descartados: pd.DataFrame) -> dict:
    conteo_motivos = (
        df_descartados["MOTIVO_DESCARTE"].value_counts().to_dict()
        if "MOTIVO_DESCARTE" in df_descartados.columns
        else {}
    )
    return {
        "Registros Crudos": total_crudos,
        "Registros Validos": len(df_validos),
        "Duplicados CRM": conteo_motivos.get("DUPLICADO_CRM", 0),
        "Duplicados Archivo": conteo_motivos.get("DUPLICADO_ARCHIVO", 0),
        "Sin Documento": conteo_motivos.get("SIN_DOCUMENTO", 0),
        "Sin Email": conteo_motivos.get("SIN_EMAIL", 0),
        "Total Descartados": len(df_descartados),
    }


def build_audit_log(corrections_prospeccion: list, corrections_crm: list, kpis: dict) -> pd.DataFrame:
    """Arma un log plano (Seccion, Campo, Valor) para la hoja de auditoria."""
    filas = []

    for correccion in corrections_prospeccion:
        filas.append(
            ("Cabecera Base Prospeccion", correccion["original"], correccion["normalizado"])
        )

    for correccion in corrections_crm:
        filas.append(("Cabecera Base CRM", correccion["original"], correccion["normalizado"]))

    for clave, valor in kpis.items():
        filas.append(("KPI", clave, valor))

    return pd.DataFrame(filas, columns=["Seccion", "Campo", "Valor"])
