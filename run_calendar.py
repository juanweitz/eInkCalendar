import time

import schedule

import displayRun


def main():
    schedule.every().day.at("00:00").do(displayRun.main)
    schedule.every(10).minutes.do(displayRun.main)

    displayRun.main()
    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == '__main__':
    main()
