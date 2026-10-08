import pandas as pd

from core.matcher import match_crm


def test_match_crm_marca_coincidencias():
    df = pd.DataFrame({"NUMERO_DOCUMENTO": ["111", "222", "333"]})
    crm_df = pd.DataFrame({"NUMERO_DOCUMENTO": ["222", "999"]})

    resultado = match_crm(df, crm_df, ["NUMERO_DOCUMENTO"])

    assert resultado.tolist() == [False, True, False]


def test_match_crm_sin_columna_en_crm_no_rompe():
    df = pd.DataFrame({"NUMERO_DOCUMENTO": ["111"]})
    crm_df = pd.DataFrame({"OTRA_COL": ["x"]})

    resultado = match_crm(df, crm_df, ["NUMERO_DOCUMENTO"])

    assert resultado.tolist() == [False]
