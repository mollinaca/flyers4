# flake8: noqa

import json
import os
import requests
from bs4 import BeautifulSoup
import lib
import config as c


def get_flyers_pages_url(shop: str) -> dict:
    """
    tokubai 店舗別チラシページからチラシページURLを取得する
    """
    ret = {"ok": False}
    base_url = "https://tokubai.co.jp"
    urls = []
    url = c.target[shop]

    try:
        UA = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/93.0.4577.63 Safari/537.36"
        )

        headers = {'User-Agent': UA}
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        html = BeautifulSoup(res.content, 'html.parser')
        elements = html.find_all(class_='image_element')
        for e in elements:
            e2 = f'<html><body>{e}</body></html>'
            s = BeautifulSoup(e2, 'html.parser')
            link = s.find('a', class_='image_element')
            if link and 'href' in link.attrs:
                urls.append(base_url + link['href'])

    except Exception as e:
        ret = {"ok": False, "e": str(e)}
        return ret

    ret = {"ok": True, "urls": urls}
    return ret


def get_flyer_url(url: str) -> dict:
    """
    tokubai 各チラシページからチラシURLを取得する
    （前提）１ページに１枚
    """
    ret = {"ok": False}

    try:
        UA = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/93.0.4577.63 Safari/537.36"
        )

        headers = {'User-Agent': UA}
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        html = BeautifulSoup(res.content, 'html.parser')
        view_state = html.find('div', {'id': 'view_state'})['data-view-state']
        data = json.loads(view_state)
        current_leaflet_high_res_image_url = (
            data['current_leaflet']['high_resolution_image_url']
            .split("?")[0]
        )

    except Exception as e:
        ret = {"ok": False, "e": str(e)}
        return ret

    ret = {"ok": True, "url": current_leaflet_high_res_image_url}
    return ret


def main(shop: str, last_json: dict) -> dict:
    ret = {"ok": False}
    latest_upload = []

    res = get_flyers_pages_url(shop)
    if not res["ok"]:
        return res
    flyer_page_urls = res["urls"]

    flyer_urls = []
    for page_url in flyer_page_urls:
        url = get_flyer_url(page_url)
        flyer_urls.append(url["url"])

    for url in flyer_urls:
        if shop in last_json and url in last_json[shop]:
            latest_upload.append(url)
        else:
            p = lib.dl(url)
            if p["ok"]:
                p = p["filename"]
            else:
                ret = {"ok": False, "p": p}

            slack_client = lib.SlackAPI()
            res1 = slack_client.upload_file_to_slack(p, shop)
            discord_client = lib.DiscordAPI()
            res2 = discord_client.upload_file_to_discord(p, shop)

            if res1["ok"] and res2["ok"]:
                latest_upload.append(url)
                if c.logging_enable:
                    lib.logging(c.logfile_name, f"shop: {shop}, uploaded_filename : {p}, upload_flyer_url : {url}")
            os.remove(p)

    ret = {"ok": True, "latest_upload": latest_upload}
    return ret
