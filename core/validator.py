"""Validacion de estructura del archivo de prospeccion."""

import pandas as pd


class ValidationError(Exception):
    """Error de validacion de estructura sobre un archivo cargado."""


def validate_structure(df: pd.DataFrame, required_columns: list[str]) -> None:
    """Verifica que, luego de normalizar cabeceras, esten las columnas obligatorias.

    Lanza ValidationError con el detalle de columnas faltantes si corresponde.
    """
    if df.empty:
        raise ValidationError("El archivo no contiene filas de datos.")

    faltantes = [col for col in required_columns if col not in df.columns]
    if faltantes:
        raise ValidationError(
            "Faltan columnas obligatorias luego de la normalizacion: "
            + ", ".join(faltantes)
        )
