import os
import json


def create_envs_from_secret(secret_key: str):
    #secrets_file = "/var/run/secrets/secrets"

    #with open(secrets_file) as file:
    #    envs = json.loads(file.read())

    envs = json.loads(os.environ["secrets"])

    for key, value in envs.items():
        if isinstance(value, dict):
            os.environ[key] = json.dumps(value)
        else:
            os.environ[key] = value
