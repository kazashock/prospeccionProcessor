import pandas as pd

from core.normalizer import normalize_data, normalize_headers


def test_normalize_headers_aliases(headers_config):
    df = pd.DataFrame(
        columns=["Mail", "DNI", "Nombre", "Apellido", "Telefono"]
    )

    df_renamed, corrections = normalize_headers(df, headers_config)

    assert list(df_renamed.columns) == ["EMAIL", "NUMERO_DOCUMENTO", "NOMBRE", "APELLIDO", "Telefono"]
    originals = {c["original"] for c in corrections}
    assert originals == {"Mail", "DNI", "Nombre", "Apellido"}


def test_normalize_headers_no_changes_when_already_canonical(headers_config):
    df = pd.DataFrame(columns=["NUMERO_DOCUMENTO", "EMAIL"])

    df_renamed, corrections = normalize_headers(df, headers_config)

    assert list(df_renamed.columns) == ["NUMERO_DOCUMENTO", "EMAIL"]
    assert corrections == []


def test_normalize_headers_duplicate_alias_is_flagged(headers_config):
    df = pd.DataFrame(columns=["Mail", "E-mail"])

    df_renamed, corrections = normalize_headers(df, headers_config)

    assert list(df_renamed.columns) == ["EMAIL", "E-mail"]
    assert any("ignorada" in c["normalizado"] for c in corrections)


def test_normalize_data_cleans_documento_y_email():
    df = pd.DataFrame(
        {
            "NUMERO_DOCUMENTO": [" 30.111.222 ", "", None],
            "EMAIL": [" Persona@Mail.com ", "", None],
            "NOMBRE": [" Juan ", "", None],
        }
    )

    result = normalize_data(df)

    assert result["NUMERO_DOCUMENTO"].tolist()[0] == "30111222"
    assert pd.isna(result["NUMERO_DOCUMENTO"].iloc[1])
    assert result["EMAIL"].tolist()[0] == "persona@mail.com"
    assert pd.isna(result["EMAIL"].iloc[1])
    assert result["NOMBRE"].tolist()[0] == "Juan"
