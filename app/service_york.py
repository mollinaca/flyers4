import os
import requests
from bs4 import BeautifulSoup
import lib
import config as c

def get_flyers_url(shop: str) -> dict:
    """
    ヨークマートチラシの店舗ページから、チラシ単位のURL一覧をリストで取得する
    """
    base_url = "https://www.york-inc.com"
    ret = {"ok": False}
    urls = []

    try:
        res = requests.get(c.target[shop])
        html = BeautifulSoup(res.content.decode('utf-8'), "html.parser")
        elements = html.find_all(class_='store-details-viewer__display__item js-store-viewer__image')
        file_paths = []
        for element in elements:
            img_tag = element.find('img')
            if img_tag and img_tag.has_attr('src') and img_tag['src'].endswith('.jpg'):
                file_paths.append(img_tag['src'])

        for file_path in file_paths:
            urls.append(base_url + file_path)

    except Exception as e:
        ret = {"ok": False, "e": str(e)}
        return ret

    ret = {"ok": True, "urls": urls}
    return ret


def main(shop:str, last_json:dict) -> dict:
    ret = {"ok": False}
    latest_upload = []

    res = get_flyers_url(shop)
    if not res["ok"]:
        return res

    for url in res["urls"]:
        if url in last_json[shop]:
            print ("already uploaded")
            latest_upload.append(url)
        else:
            p = lib.dl(url)
            slack_client = lib.SlackAPI()
            res = slack_client.upload_file_to_slack(p)
            print (res)
            os.remove(p)
            latest_upload.append(url)

    ret = {"ok": True, "latest_upload": latest_upload}
    return ret
