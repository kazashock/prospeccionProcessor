"""Reglas de descarte: SIN_DOCUMENTO, SIN_EMAIL, DUPLICADO_ARCHIVO, DUPLICADO_CRM."""

import pandas as pd


def apply_discard_rules(df: pd.DataFrame, en_crm: pd.Series, rules_config: dict):
    """Aplica las reglas de descarte en el orden de prioridad configurado.

    Devuelve (df_validos, df_descartados). df_descartados incluye la columna
    MOTIVO_DESCARTE con el primer motivo (segun prioridad) que aplico a la fila.
    """
    df = df.copy()
    motivo = pd.Series(pd.NA, index=df.index, dtype="string")

    reasons_masks = {}

    if "NUMERO_DOCUMENTO" in df.columns:
        reasons_masks["SIN_DOCUMENTO"] = df["NUMERO_DOCUMENTO"].isna()

    if "EMAIL" in df.columns:
        reasons_masks["SIN_EMAIL"] = df["EMAIL"].isna()

    dup_keys = [k for k in rules_config.get("duplicate_file_keys", []) if k in df.columns]
    if dup_keys:
        sin_datos = df[dup_keys].isna().any(axis=1)
        reasons_masks["DUPLICADO_ARCHIVO"] = df.duplicated(subset=dup_keys, keep="first") & ~sin_datos

    reasons_masks["DUPLICADO_CRM"] = en_crm.reindex(df.index, fill_value=False)

    for reason in rules_config.get("discard_priority", []):
        mask = reasons_masks.get(reason)
        if mask is None:
            continue
        aplica = mask & motivo.isna()
        motivo = motivo.mask(aplica, reason)

    df["MOTIVO_DESCARTE"] = motivo

    df_validos = df.loc[motivo.isna()].drop(columns=["MOTIVO_DESCARTE"]).reset_index(drop=True)
    df_descartados = df.loc[motivo.notna()].reset_index(drop=True)

    return df_validos, df_descartados
