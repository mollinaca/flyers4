#!/usr/bin/env python3
import json
import os
import lib
import config as c
import service_york, service_gs, service_tokubai

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
            # pass
            ret = service_york.main(shop, last_json)
            if ret["ok"]:
                latest_json[shop] = ret["latest_upload"]
            else:
                latest_json[shop] = last_json[shop]

        elif shop == "業務スーパー":
            # pass
            ret = service_gs.main(shop, last_json)
            if ret["ok"]:
                latest_json[shop] = ret["latest_upload"]
            else:
                latest_json[shop] = last_json[shop]

        elif shop == "マミーマート":
            # pass
            ret = service_tokubai.main(shop, last_json)
            if ret["ok"]:
                latest_json[shop] = ret["latest_upload"]
            else:
                latest_json[shop] = last_json[shop]

        else:
            pass

    os.remove(LAST_JSON_PATH)
    with open(LAST_JSON_PATH, 'w', encoding="utf-8") as f:
        json.dump(latest_json, f, indent=4, ensure_ascii=False)


    return 0

if __name__ == '__main__':
  main()
