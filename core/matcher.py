"""Cruce de la base de prospeccion contra la base exportada del CRM."""

import pandas as pd


def match_crm(df: pd.DataFrame, crm_df: pd.DataFrame, match_keys: list[str]) -> pd.Series:
    """Devuelve una Serie booleana (misma longitud que df) marcando EN_CRM=True
    para las filas cuyo valor en alguna de las match_keys ya existe en crm_df.

    Las columnas de match_keys deben existir y venir ya normalizadas (mismo
    formato de limpieza) en ambos dataframes.
    """
    en_crm = pd.Series(False, index=df.index)

    for key in match_keys:
        if key not in df.columns or key not in crm_df.columns:
            continue
        valores_crm = set(crm_df[key].dropna().astype(str))
        valores_crm.discard("")
        en_crm = en_crm | df[key].astype(str).isin(valores_crm)

    return en_crm
