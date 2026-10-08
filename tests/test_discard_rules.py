import pandas as pd

from core.discard_rules import apply_discard_rules


def test_apply_discard_rules_prioridad(rules_config):
    df = pd.DataFrame(
        {
            "NUMERO_DOCUMENTO": [pd.NA, "111", "111", "222", "333"],
            "EMAIL": ["a@a.com", pd.NA, "b@b.com", "c@c.com", "d@d.com"],
            "NOMBRE": ["A", "B1", "B2", "C", "D"],
            "APELLIDO": ["A", "B", "B", "C", "D"],
        }
    )
    en_crm = pd.Series([False, False, False, False, True], index=df.index)

    df_validos, df_descartados = apply_discard_rules(df, en_crm, rules_config)

    motivos = dict(zip(df_descartados["NOMBRE"], df_descartados["MOTIVO_DESCARTE"]))
    assert motivos["A"] == "SIN_DOCUMENTO"
    assert motivos["B1"] == "SIN_EMAIL"
    assert motivos["B2"] == "DUPLICADO_ARCHIVO"
    assert motivos["D"] == "DUPLICADO_CRM"
    assert len(df_validos) == 1
    assert df_validos.iloc[0]["NOMBRE"] == "C"


def test_apply_discard_rules_duplicado_archivo(rules_config):
    df = pd.DataFrame(
        {
            "NUMERO_DOCUMENTO": ["111", "111"],
            "EMAIL": ["a@a.com", "b@b.com"],
            "NOMBRE": ["Primero", "Segundo"],
            "APELLIDO": ["X", "Y"],
        }
    )
    en_crm = pd.Series([False, False], index=df.index)

    df_validos, df_descartados = apply_discard_rules(df, en_crm, rules_config)

    assert len(df_validos) == 1
    assert df_validos.iloc[0]["NOMBRE"] == "Primero"
    assert df_descartados.iloc[0]["MOTIVO_DESCARTE"] == "DUPLICADO_ARCHIVO"
