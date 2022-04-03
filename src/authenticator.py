import pyotp
import os
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = f"{ROOT_DIR}/../secret_keys.json"


class Authenticator:
    accounts = []

    def __init__(self):
        with open(CONFIG_DIR, "r") as f:
            data = json.load(f)
            for item in data:
                self.accounts.append(
                    {"name": item["name"], "code_gener": pyotp.totp.TOTP(item["code"])}
                )
        print(self.accounts)

    def save_secret(self, secret_code: str):
        print("ok")

    def get_code(self, name):
        for item in self.accounts:
            if item["name"] == name:
                return item["code_gener"].now()
        return ''
