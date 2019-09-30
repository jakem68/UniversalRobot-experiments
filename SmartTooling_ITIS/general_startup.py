#!/usr/bin/env python

__author__ = 'Jan Kempeneers'

import threading, socketComm_ppau
from subprocess import call


def run():
    thread_socketComm_ppau = threading.Thread(target=socketComm_ppau.run)
    thread_socketComm_ppau.start()
    # thread2 = threading.Thread(target=dweet_actions, args=(q,))
    # thread2.start()


def main():
    run()


if __name__ == "__main__":
    main()
