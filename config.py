PROJECT = "teamia-prod-df3d"

DATASET = "ia_tjenester_metrikker"

TABLE = "IA-tjenester-metrikker"

SQL_QUERY = f"SELECT  * FROM `{PROJECT}.{DATASET}.{TABLE}`"

DATASTORY_DEV = "https://nada.intern.dev.nav.no/api"
DATASTORY_PROD = "https://nada.intern.nav.no/api"

TOKEN_SECRET_KEY = "DATASTORY_TOKEN"
