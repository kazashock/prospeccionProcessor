import pandas as pd
import pytest

from core.validator import ValidationError, validate_structure


def test_validate_structure_ok(rules_config):
    df = pd.DataFrame(
        {
            "NUMERO_DOCUMENTO": ["1"],
            "EMAIL": ["a@a.com"],
            "NOMBRE": ["Juan"],
            "APELLIDO": ["Perez"],
        }
    )

    validate_structure(df, rules_config["required_columns"])


def test_validate_structure_faltante(rules_config):
    df = pd.DataFrame({"NUMERO_DOCUMENTO": ["1"], "EMAIL": ["a@a.com"]})

    with pytest.raises(ValidationError, match="NOMBRE"):
        validate_structure(df, rules_config["required_columns"])


def test_validate_structure_vacio(rules_config):
    df = pd.DataFrame(columns=rules_config["required_columns"])

    with pytest.raises(ValidationError):
        validate_structure(df, rules_config["required_columns"])
