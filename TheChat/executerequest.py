import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


class eazybase:
    def __init__(self, phone: str, company_owner: str):
        self.base_url = os.getenv("CHAT_URL")
        self.gdata_url = os.getenv("GDATA_URL")
        self.login_url = os.getenv("LOGIN_URL")
        self.getsources = os.getenv("SHOW_SOURCES")
        self.phone = phone
        self.email = ""
        self.company_owner = company_owner
        self.profile_name = f"Guest - {self.phone}"
        self.logindone = False
        self.requested = False
        self.current_gdata = []

    def isLogged(self):
        return self.logindone

    def isrequested(self):
        return self.requested

    def gather_data(self):
        return True

    def do_login(self, phone_num, code):
        self.phone = phone_num
        json_ = {"mapData": {"phone": self.phone, "code": code}}
        return_data = self._submit_request(json_, self.login_url, "sentLink")
        if return_data["action"] == "code_sent":
            self.requested = True
        if return_data["action"] == "login":
            self.requested = True
            self.logindone = True
            self.profile_name = return_data["name"]
            self.emaili = return_data["email"]

    def get_text_description(self, mapgdata) -> str:
        str_base = f'Date: {mapgdata["created_dt"]} - Executed: {mapgdata["kbase"]}'
        for needs_gathering in mapgdata["gschema"]:
            if needs_gathering["key"] in mapgdata["gdata"]:
                str_base += f"\n {needs_gathering['description']} : {mapgdata['gdata'][needs_gathering['key']]}"

        return str_base

    def _get_usr_gatherdata(self):
        json_ = {"mapData": {"phone": self.phone, "profile_name": self.profile_name}}
        self.current_gdata = self._submit_request(json_, self.gdata_url, "usageData")
        print(self.current_gdata)

    def _submit_request(self, json_, url: str, return_str: str) -> dict:
        req = requests.post(url, data=json.dumps(json_))
        chat_return = req.json()
        if isinstance(chat_return[return_str], str):
            return json.loads(chat_return[return_str])
        return chat_return[return_str]

    def GetResponse(self, prompt: str) -> str:
        json_ = {
            "rawdata": {
                "companyowner": self.company_owner,
                "phone": self.phone,
                "body": prompt,
                "profile_name": self.profile_name,
                "fetch_sources": self.getsources,
            }
        }

        return_data = self._submit_request(json_, self.base_url, "chatreturn")
        print(type(return_data))
        print(return_data["response_body"])
        print(return_data["kbase"])
        return (
            return_data["response_body"],
            return_data["kbase"],
        )
