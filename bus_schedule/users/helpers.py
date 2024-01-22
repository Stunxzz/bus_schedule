import base64
import json

import requests


class LdapBase:
    def __init__(self, app_name, url, user, password):
        self.url = url
        self.app_name = app_name
        self.user = user
        self.password = password


class LdapHashBase64:
    @staticmethod
    def base64_hash(user, password):
        secret = {"username": user, "password": password}
        secret = str(base64.b64encode(json.dumps(secret).encode("ascii")))
        secret = secret[2:-1]  # clear b'' from string
        return secret


class LdapContent(LdapBase, LdapHashBase64):
    def __init__(self, app_name, url, user, password):
        super().__init__(app_name, url, user, password)

    def data(self):
        return {"access": self.app_name}

    def headers(self):
        secret = self.base64_hash(self.user, self.password)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {secret}",
        }
        return headers


class LdapResponse(LdapContent):
    def get_response(self):
        url = self.url
        headers = self.headers()
        data = self.data()
        response = requests.post(url=url, headers=headers, json=data)
        return response


class LdapStatusCode(LdapResponse):

    def get_status_code(self):
        response = self.get_response()
        status = response.status_code
        return status


class LdapUserData(LdapResponse):
    def json_response(self):
        response = self.get_response().json()["userdata"]
        return response


class LdapUserAttributes(LdapUserData):
    def get_username(self):
        username = self.json_response()["username"]
        return username

    def get_first_name(self):
        first_name = self.json_response()["name"]
        return first_name

    def get_last_name(self):
        last_name = self.json_response()["last"]
        return last_name

    def get_personal_number(self):
        personal_number = self.json_response()["pin"]
        return personal_number

    def get_email(self):
        email = self.json_response()["email"]
        return email

    def get_all_attributes(self):
        username = self.get_username()
        first_name = self.get_first_name()
        last_name = self.get_last_name()
        personal_number = self.get_personal_number()
        email = self.get_email()
        return username, first_name, last_name, personal_number, email
