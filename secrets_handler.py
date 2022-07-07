import os
import json


def create_envs_from_secret(secret_key: str):
    envs = json.loads(os.environ[secret_key])
    for key, value in envs.items():
        if isinstance(value, dict):
            os.environ[key] = json.dumps(value)
        else:
            os.environ[key] = value
