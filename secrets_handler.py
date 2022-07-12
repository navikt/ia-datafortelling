import os
import json


def create_envs_from_secret(secret_key: str):
    secrets_file = "/var/run/secrets/ia-tjenester-metrikker-datafortelling-secrets/secret"

    with open(secrets_file) as file:
        envs = json.loads(file.read())

    # envs = json.loads(os.environ["IA_METRIKKER_ENVS"])

    for key, value in envs.items():
        if isinstance(value, dict):
            os.environ[key] = json.dumps(value)
        else:
            os.environ[key] = value
