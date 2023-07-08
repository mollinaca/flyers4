#!/usr/bin/env python3
import lib

def main():

    slack_clinet = lib.SlackAPI()
    res = slack_clinet.iwebhook("test message")
    return 0




if __name__ == '__main__':
  main()
