"""Genera Excels sinteticos de ejemplo (BaseProspeccion y export CRM) para
probar la app manualmente. Uso: python scripts/generate_sample_data.py
"""

from pathlib import Path

import pandas as pd

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "sample"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    base_prospeccion = pd.DataFrame(
        {
            "Nombre": ["Ana", "Beto", "Carla", "Dario", "Elena", "Fabio", "Fabio", "Gina", "Hugo", "Ines"],
            "Apellido": ["Perez", "Gomez", "Diaz", "Lopez", "Ruiz", "Sosa", "Sosa", "Vega", "Paz", "Cruz"],
            "DNI": [
                "30111222",
                "30222333",
                "30333444",
                "",
                "30555666",
                "30666777",
                "30666777",
                "30777888",
                "30888999",
                "30999000",
            ],
            "e-mail": [
                "ana.perez@mail.com",
                "beto.gomez@mail.com",
                "",
                "dario.lopez@mail.com",
                "elena.ruiz@mail.com",
                "fabio.sosa@mail.com",
                "fabio.sosa@mail.com",
                "gina.vega@mail.com",
                "hugo.paz@mail.com",
                "ines.cruz@mail.com",
            ],
            "Telefono": [
                "1122334455",
                "1133445566",
                "1144556677",
                "1155667788",
                "1166778899",
                "1177889900",
                "1177889900",
                "1188990011",
                "1199001122",
                "1100112233",
            ],
        }
    )

    base_crm = pd.DataFrame(
        {
            "Numero Documento": ["30777888", "30999000"],
            "Mail": ["gina.vega@mail.com", "ines.cruz@mail.com"],
        }
    )

    base_prospeccion.to_excel(OUTPUT_DIR / "BaseProspeccion_ejemplo.xlsx", index=False)
    base_crm.to_excel(OUTPUT_DIR / "CRM_export_ejemplo.xlsx", index=False)

    print(f"Archivos generados en {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
