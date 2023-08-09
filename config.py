PROJECT = "teamia-prod-df3d"

DATASET = "ia_tjenester_metrikker"

TABLE = "IA-tjenester-metrikker"

SQL_QUERY = f"SELECT  * FROM `{PROJECT}.{DATASET}.{TABLE}`"

DATASTORY_DEV = "https://data.ekstern.dev.nav.no/api"
DATASTORY_PROD = "https://data.nav.no/api"

TOKEN_SECRET_KEY = "DATASTORY_TOKEN"
