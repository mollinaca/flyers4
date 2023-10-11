#!/usr/bin/env python3
import json
import os
import config as c
import service_york
import service_gs
import service_tokubai


def main():

    TARGET = c.target

    if c.development_mode:
        LAST_JSON_PATH = "data/last_dev.json"
    else:
        LAST_JSON_PATH = "data/last.json"

    with open(LAST_JSON_PATH, 'r') as f:
        last_json = json.load(f)
    latest_json = {}

    for shop in TARGET:
        if shop == "ヨークマート":
            # ret = {"ok": False}
            ret = service_york.main(shop, last_json)

        elif shop == "業務スーパー":
            # ret = {"ok": False}
            ret = service_gs.main(shop, last_json)

        elif (shop == "マミーマート") or (shop == "マツモトキヨシ") or (shop == "コープ"):
            # ret = {"ok": False}
            ret = service_tokubai.main(shop, last_json)

        else:
            pass

        if ret["ok"]:
            latest_json[shop] = ret["latest_upload"]
        else:
            latest_json[shop] = last_json[shop]

    os.remove(LAST_JSON_PATH)
    with open(LAST_JSON_PATH, 'w', encoding="utf-8") as f:
        json.dump(latest_json, f, indent=4, ensure_ascii=False)

    return 0


if __name__ == '__main__':
    main()
