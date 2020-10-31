import gathering_current_data
import time

INTERVALS_HOUR = 3


def main():
    wait_time_sec = INTERVALS_HOUR * 60 * 60
    while True:
        gathering_current_data.main()
        time.sleep(wait_time_sec)


if __name__ == '__main__':
    main()
