#!/usr/bin/env python3
import json
import lib
import config
import service_york

def main():

    TARGET = config.target
    print (TARGET)

    LAST_JSON_PATH = "data/last.json"
    with open(LAST_JSON_PATH) as f:
      last_json = json.load(f)

    for shop in TARGET:
      print (shop, TARGET[shop])
      if shop == "ヨークマート":
        print (shop)
        ret = service_york.main()

        slack_client = lib.SlackAPI()
        ret = slack_client.iwebhook(str(ret))
        print (res)

        exit (1)
      else:
        pass


    slack_client = lib.SlackAPI()
    res = slack_client.iwebhook("test message")
    return 0




if __name__ == '__main__':
  main()
