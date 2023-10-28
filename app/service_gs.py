# flake8: noqa

import os
import time
import requests
import hashlib
import lib
from bs4 import BeautifulSoup
import config as c


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


def get_flyer_1() -> dict:
    """
    https://www.gyomusuper.jp/images/bargain_east.pdf
    をDLして、ファイルパスを返す
    """
    ret = {"ok": False}

    url = "https://www.gyomusuper.jp/images/bargain_east.pdf"
    res = get_flyer_url_alive(url)
    if not res["ok"]:
        ret = {"ok": False, "error": "get_flyer_url_alive -> False"}
        return ret

    time.sleep(1)
    p = lib.dl(url)
    if p["ok"]:
        p = p["filename"]
        ret = {"ok": True, "p": p}
    else:
        ret = {"ok": False, "p": p}

    return ret


def get_flyer_2() -> dict:
    """
    https://www.gyomusuper.jp/sale/kanto.html#%E5%9F%BC%E7%8E%89%E7%9C%8C
    このページから取得できるチラシをDLして、ファイルパスをリストで返す
    """
    ret = {"ok": False, "p_list": []}

    url = "https://www.gyomusuper.jp/sale/kanto.html#%E5%9F%BC%E7%8E%89%E7%9C%8C"
    res = get_flyer_url_alive(url)
    if not res["ok"]:
        ret = {"ok": False, "error": "get_flyer_url_alive -> False"}
        return ret

    time.sleep(1)

    urls = get_flyer_2_urls()
    ps = []
    for url in urls["urls"]:
        p = lib.dl(url)
        if p["ok"]:
            ps.append(p["filename"])
        else:
            ret = {"ok": False}
            return ret

    ret = {"ok": True, "ps": ps}
    return ret


def get_flyer_2_urls() -> list:
    """
    https://www.gyomusuper.jp/sale/kanto.html#%E5%9F%BC%E7%8E%89%E7%9C%8C
    このページのチラシURL一覧を取得してリストで返す
    """
    ret = {"ok": False}
    base_url = "https://www.gyomusuper.jp/sale/"
    url = "https://www.gyomusuper.jp/sale/kanto.html#%E5%9F%BC%E7%8E%89%E7%9C%8C"

    try:
        res = requests.get(url)
        html = BeautifulSoup(res.content.decode('utf-8'), "html.parser")
        item_list = html.find("ul", class_="item_list")
        urls = []

        if item_list:
            img_tags = item_list.find_all("img")

            for img_tag in img_tags:
                src = img_tag.get("src")
                if src:
                    if src.endswith('?2'):
                        src = src[:-2]
                    urls.append(base_url + src)

    except Exception as e:
        ret = {"ok": False, "e": str(e)}
        return ret

    ret = {"ok": True, "urls": urls}
    return ret


def main(shop: str, last_json: dict) -> dict:
    ret = {"ok": False}
    latest_upload = []

    # get_flyer_1
    res = get_flyer_1()
    if not res["ok"]:
        lib.logging(c.logfile_name, f"get_flyer_1() return error : {res['e']}")
    else:
        p = res["p"]
        h = hashlib.md5()
        with open(p, 'rb') as hash_file:
            r_hash = hash_file.read()
            h.update(r_hash)
            hash_digest = h.hexdigest()

        if (shop in last_json and hash_digest not in last_json[shop]) or \
           (shop not in last_json):
            slack_client = lib.SlackAPI()
            res = slack_client.upload_file_to_slack(p, shop)
            if res["ok"]:
                latest_upload.append(hash_digest)
                if c.logging_enable:
                    lib.logging(c.logfile_name, f"shop: {shop}, uploaded_filename : {p}, upload_flyer_hash : {hash_digest}")
        else:
            latest_upload.append(hash_digest)

        os.remove(p)

    # get_flyer_2
    res = get_flyer_2()
    if not res["ok"]:
        lib.logging(c.logfile_name, f"get_flyer_2() return error : ${res['e']}")
    else:
        ps = res["ps"]

        for p in ps:
            h = hashlib.md5()
            with open(p, 'rb') as hash_file:
                r_hash = hash_file.read()
                h.update(r_hash)
                hash_digest = h.hexdigest()

            if (shop in last_json and hash_digest not in last_json[shop]) or \
               (shop not in last_json):
                slack_client = lib.SlackAPI()
                res = slack_client.upload_file_to_slack(p, shop)
                if res["ok"]:
                    latest_upload.append(hash_digest)
                    if c.logging_enable:
                        lib.logging(c.logfile_name, f"shop: {shop}, uploaded_filename : {p}, upload_flyer_hash : {hash_digest}")

            else:
                latest_upload.append(hash_digest)

            os.remove(p)

    ret = {"ok": True, "latest_upload": latest_upload}
    return ret
