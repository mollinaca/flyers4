#!/usr/bin/env python3
import json
import sys
import os
import shutil
import requests
from dotenv import load_dotenv
from slack_sdk import WebhookClient, WebClient
from slack_sdk.errors import SlackApiError
load_dotenv()

def dl(url: str) -> str:
    """
    download file and return filename
    """
    filename = os.path.basename(url)

    if 64 < len(filename):
        filename = filename[:60] + filename.split(".")[-1]

    res = requests.get(url, stream=True)

    with open(filename, mode="wb") as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)

    return filename

class SlackAPI():

    def iwebhook(self, message:str = "None") -> dict:
        ret = {"ok": False}

        # client = WebhookClient(token=os.environ["SLACK_WEBHOOK_URL"])
        client = WebhookClient(os.environ["SLACK_WEBHOOK_URL_DEV"])
        try:
            response = client.send(text=message)
            assert response.status_code == 200
            assert response.body == "ok"
            ret = {"ok": True, "response": response}

        except Exception as e:
            ret = {"ok": False, "exception": str(e)}

        return ret

    def upload_file_to_slack(self, filepath:str = "None") -> dict:
        ret = {"ok": False}
        client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
        try:
            # response = client.files_upload_v2(channel=os.environ["SLACK_CHANNEL_ID"], file=filepath)
            response = client.files_upload_v2(channel=os.environ["SLACK_CHANNEL_ID_DEV"], file=filepath)
            assert response["file"]
            ret = {"ok": True, "response": response}

        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            ret = {"ok": False, "exception": str(e)}

        except Exception as e:
            ret = {"ok": False, "exception": str(e)}

        return ret
