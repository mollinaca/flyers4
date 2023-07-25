import os
import time
import requests
import hashlib
import lib


def get_flyer_url_alive(url: str) -> dict:
    ret = {"ok": False}
    try:
        response = requests.get(url)
        if response.status_code // 100 == 2:
            ret = {"ok": True}
            return ret
        else:
            ret = {"ok": False, "status_code": response.status_code}
            return ret

    except requests.exceptions.RequestException as e:
        ret = {"ok": False, "e": str(e)}
        return ret


def main(shop: str, last_json: dict) -> dict:
    ret = {"ok": False}
    latest_upload = []
    url = "https://www.gyomusuper.jp/images/bargain_east.pdf"

    res = get_flyer_url_alive(url)
    if not res["ok"]:
        ret = {"ok": False, "error": "get_flyer_url_alive -> False"}
        return ret
    time.sleep(1)
    p = lib.dl(url)
    if p["ok"]:
        p = p["filename"]
    else:
        ret = {"ok": False, "p": p}
        return ret

    h = hashlib.md5()
    with open(p, 'rb') as hash_file:
        r_hash = hash_file.read()
        h.update(r_hash)
        hash_digest = h.hexdigest()

    if hash_digest not in last_json[shop]:
        slack_client = lib.SlackAPI()
        res = slack_client.upload_file_to_slack(p, shop)
        if res["ok"]:
            latest_upload.append(hash_digest)

    os.remove(p)
    ret = {"ok": True, "latest_upload": latest_upload}
    return ret
