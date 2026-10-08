"""Normalizacion de cabeceras y datos de la base de prospeccion."""

import re
import unicodedata

import pandas as pd


def _slug(value: str) -> str:
    value = str(value).strip().lower()
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", " ", value).strip()
    return value


def build_alias_lookup(headers_config: dict) -> dict:
    """Mapea cada alias (y el propio nombre canonico) normalizado -> nombre canonico."""
    lookup = {}
    for canonical, aliases in headers_config.items():
        lookup[_slug(canonical)] = canonical
        for alias in aliases:
            lookup[_slug(alias)] = canonical
    return lookup


def normalize_headers(df: pd.DataFrame, headers_config: dict):
    """Renombra columnas segun headers_config.

    Devuelve (df_renombrado, corrections) donde corrections es una lista de
    dicts {"original": ..., "normalizado": ...} con cada cambio detectado.
    """
    lookup = build_alias_lookup(headers_config)
    rename_map = {}
    corrections = []
    used_targets = set()

    for column in df.columns:
        slug = _slug(column)
        target = lookup.get(slug)
        if target is None:
            continue
        if target in used_targets:
            corrections.append(
                {
                    "original": column,
                    "normalizado": f"(ignorada, {target} ya fue asignada)",
                }
            )
            continue
        used_targets.add(target)
        if column != target:
            rename_map[column] = target
            corrections.append({"original": column, "normalizado": target})

    df_renamed = df.rename(columns=rename_map)
    return df_renamed, corrections


def _clean_text(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip()


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia los valores de las columnas canonicas conocidas."""
    df = df.copy()

    if "NUMERO_DOCUMENTO" in df.columns:
        df["NUMERO_DOCUMENTO"] = (
            _clean_text(df["NUMERO_DOCUMENTO"])
            .str.replace(r"[^0-9]", "", regex=True)
            .replace("", pd.NA)
        )

    if "EMAIL" in df.columns:
        df["EMAIL"] = _clean_text(df["EMAIL"]).str.lower().replace("", pd.NA)

    for column in ("NOMBRE", "APELLIDO"):
        if column in df.columns:
            df[column] = _clean_text(df[column]).replace("", pd.NA)

    return df
