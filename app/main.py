#!/usr/bin/env python3
import json
import lib
import config

def main():

    TARGET = config.target
    print (TARGET)

    LAST_JSON_PATH = "data/last.json"
    with open(LAST_JSON_PATH) as f:
      last_json = json.load(f)

    for shop in TARGET:
      print (shop, TARGET[shop])


    slack_clinet = lib.SlackAPI()
    res = slack_clinet.iwebhook("test message")
    return 0




if __name__ == '__main__':
  main()
