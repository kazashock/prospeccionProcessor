import pandas as pd

from core.report_generator import build_descartada_workbook, build_normalizada_workbook


def test_build_normalizada_workbook_roundtrip():
    df_validos = pd.DataFrame({"NUMERO_DOCUMENTO": ["111"], "EMAIL": ["a@a.com"]})
    audit_df = pd.DataFrame({"Seccion": ["KPI"], "Campo": ["Registros Validos"], "Valor": [1]})

    buffer = build_normalizada_workbook(df_validos, audit_df)

    sheets = pd.read_excel(buffer, sheet_name=None)
    assert set(sheets.keys()) == {"Prospeccion_Normalizada", "Auditoria"}
    assert sheets["Prospeccion_Normalizada"].iloc[0]["EMAIL"] == "a@a.com"


def test_build_descartada_workbook_roundtrip():
    df_descartados = pd.DataFrame(
        {"NUMERO_DOCUMENTO": [pd.NA], "EMAIL": ["a@a.com"], "MOTIVO_DESCARTE": ["SIN_DOCUMENTO"]}
    )

    buffer = build_descartada_workbook(df_descartados)

    sheets = pd.read_excel(buffer, sheet_name=None)
    assert "Prospeccion_Descartada" in sheets
    assert sheets["Prospeccion_Descartada"].iloc[0]["MOTIVO_DESCARTE"] == "SIN_DOCUMENTO"
