"""Test de integracion del flujo completo (sin pasar por la UI de Streamlit)."""

import pandas as pd

from core.audit import build_audit_log, compute_kpis
from core.discard_rules import apply_discard_rules
from core.matcher import match_crm
from core.normalizer import normalize_data, normalize_headers
from core.validator import validate_structure


def test_flujo_completo(headers_config, rules_config):
    df_crudo_raw = pd.DataFrame(
        {
            "Mail": ["a@a.com", "b@b.com", "", "c@c.com", "d@d.com"],
            "DNI": ["111", "222", "333", "222", "444"],
            "Nombre": ["Ana", "Beto", "Carla", "Beto Dup", "Dario"],
            "Apellido": ["A", "B", "C", "B", "D"],
        }
    )
    df_crm_raw = pd.DataFrame({"DNI": ["444"]})

    df, corrections_crudo = normalize_headers(df_crudo_raw, headers_config)
    crm_df, corrections_crm = normalize_headers(df_crm_raw, headers_config)

    validate_structure(df, rules_config["required_columns"])

    df = normalize_data(df)
    crm_df = normalize_data(crm_df)

    en_crm = match_crm(df, crm_df, rules_config["crm_match_keys"])
    df_validos, df_descartados = apply_discard_rules(df, en_crm, rules_config)

    kpis = compute_kpis(len(df_crudo_raw), df_validos, df_descartados)
    audit_df = build_audit_log(corrections_crudo, corrections_crm, kpis)

    assert kpis["Registros Crudos"] == 5
    assert kpis["Sin Email"] == 1
    assert kpis["Duplicados Archivo"] == 1
    assert kpis["Duplicados CRM"] == 1
    assert kpis["Registros Validos"] == 2
    assert kpis["Total Descartados"] == 3
    assert not audit_df.empty
