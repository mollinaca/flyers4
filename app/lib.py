import os
import shutil
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from slack_sdk import WebhookClient, WebClient
from slack_sdk.errors import SlackApiError
import config as c
load_dotenv()


def logging(log_file: str, message: str) -> dict:
    ret = {"ok": False}
    now = datetime.now(tz=timezone(timedelta(hours=9)))
    ft = str(now.strftime("%Y%m%d %H:%M:%S"))

    try:
        with open(log_file, "a") as file:
            file.write(f"{ft} : {message}" + "\n")
            ret = {"ok": True}
    except Exception as e:
        ret = {"ok": False, "error": str(e)}
        return ret

    return ret


def dl(url: str) -> dict:
    filename = os.path.basename(url)

    if 64 < len(filename):
        filename = filename[:60] + filename.split(".")[-1]

    try:
        res = requests.get(url, stream=True)

        with open(filename, mode="wb") as f:
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, f)

        ret = {"ok": True, "filename": filename}

    except Exception as e:
        ret = {"ok": False, "e": str(e)}

    return ret


class SlackAPI():

    def iwebhook(self, message: str = "None") -> dict:
        ret = {"ok": False}

        if c.development_mode:
            client = WebhookClient(token=os.environ["SLACK_WEBHOOK_URL_DEV"])
        else:
            client = WebhookClient(token=os.environ["SLACK_WEBHOOK_URL"])

        try:
            response = client.send(text=message)
            assert response.status_code == 200
            assert response.body == "ok"
            ret = {"ok": True, "response": response}

        except Exception as e:
            ret = {"ok": False, "exception": str(e)}

        return ret

    def upload_file_to_slack(self, filepath: str = "None", title: str = None) -> dict:
        ret = {"ok": False}
        client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

        try:
            if c.development_mode:
                response = client.files_upload_v2(
                    channel=os.environ["SLACK_CHANNEL_ID_DEV"],
                    file=filepath,
                    title=title
                    )
            else:
                response = client.files_upload_v2(
                    channel=os.environ["SLACK_CHANNEL_ID"],
                    file=filepath,
                    title=title
                    )

            assert response["file"]
            ret = {"ok": True, "response": response}

        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            ret = {"ok": False, "exception": str(e)}

        except Exception as e:
            ret = {"ok": False, "exception": str(e)}

        return ret


class DiscordAPI():

    def iwebhook(self, message: str = "None") -> dict:
        ret = {"ok": False}

        if c.development_mode:
            webhook_url = os.environ["DISCORD_WEBHOOK_URL_DEV"]
        else:
            webhook_url = os.environ["DISCORD_WEBHOOK_URL_DEV"]

        try:
            response = requests.post(webhook_url, json={"content": message})
            if response.status_code == 200 or response.status_code == 204:
                ret = {"ok": True, "response": response.text}
            else:
                ret = {"ok": False, "response": response.text}

        except Exception as e:
            ret = {"ok": False, "exception": str(e)}

        return ret

    def upload_file_to_discord(self, filepath: str = "None", title: str = None) -> dict:
        ret = {"ok": False}

        if c.development_mode:
            webhook_url = os.environ["DISCORD_WEBHOOK_URL_DEV"]
        else:
            webhook_url = os.environ["DISCORD_WEBHOOK_URL_DEV"]

        with open(filepath, "rb") as f:
            files = {"file": f}

            try:
                response = requests.post(webhook_url, files=files)
                if response.status_code == 200 or response.status_code == 204:
                    ret = {"ok": True, "response": response.text}
                else:
                    ret = {"ok": False, "response": response.text}

            except Exception as e:
                ret = {"ok": False, "exception": str(e)}

        return ret
