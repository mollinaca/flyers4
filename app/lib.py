#!/usr/bin/env python3
import json
import sys
import os
from dotenv import load_dotenv
from slack_sdk import WebhookClient
load_dotenv()

class SlackAPI():

    def iwebhook(self, message:str = "None") -> json:
        ret = {"ok": False}

        client = WebhookClient(os.environ["SLACK_WEBHOOK_URL_DEV"])
        # client = WebhookClient(os.environ["SLACK_WEBHOOK_URL"])
        try:
            response = client.send(text=message)
            assert response.status_code == 200
            assert response.body == "ok"
            ret = {"ok": True, "response": response}

        except Exception as e:
            ret = {"ok": False, "exception": str(e)}

        return ret
