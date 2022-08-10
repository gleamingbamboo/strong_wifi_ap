import os
import sys

from loguru import logger
from winwifi import WinWiFi
from win10toast_click import ToastNotifier
import settings


class Wifi:
    def __init__(self):
        self.ssid = None

    def choose_strength_ap(self, personal_ap_list):
        self.max_strength_ssid = 0
        for ap in personal_ap_list:
            if ap.strength > self.max_strength_ssid:
                self.max_strength_ssid = ap.strength
                self.ssid = ap.ssid

    def get_ap_passwd(self):
        return settings.CREDENTIALS[self.ssid]

    def connect(self):
        try:
            logger.info("Start connecting to %s", self.ssid)
            WinWiFi.connect(self.ssid)
        except Exception:
            try:
                logger.error("Failed to connect to %s", self.ssid)
                logger.info("Try again with password")
                WinWiFi.forget(self.ssid)
                WinWiFi.connect(self.ssid, self.get_ap_passwd())
            except Exception as e:
                print(e)

    def send_notify(self):
        logger.info("Initiating notification send")
        toaster = ToastNotifier()
        logger.info("Send notification to user")
        toaster.show_toast(
            f"Connect to {self.ssid}",  # title
            "Click to connect ><",  # message
            icon_path=None,  # 'icon_path'
            duration=5,
            # for how many seconds toast should be visible; None = leave notification in Notification Center
            threaded=False,
            # True = run other code in parallel; False = code execution will wait till notification disappears
            callback_on_click=self.connect  # click notification to run function
        )

    def main(self):
        try:

            current_profiles = WinWiFi.get_profiles(lambda x: None)
            ap_list = WinWiFi.scan(callback=lambda x: x)
            personal_ap_list = [ap for ap in ap_list if ap.ssid in current_profiles]
            self.choose_strength_ap(personal_ap_list)

            current_ap = WinWiFi.get_connected_interfaces()[0].ssid
            logger.info(f"Current Ap = {current_ap};Found AP with best strength {self.ssid}")
            if self.ssid != current_ap:
                logger.info(f"Found AP with better strength {self.ssid}")
                # self.connect()
                # TODO: fix this error
                self.send_notify()
        except Exception as e:
            logger.error(f"Exception{e}")


if __name__ == '__main__':
    logger.add("file_{time}.log", rotation="500 MB")
    logger.info("Starting...")
    if os.name == 'nt':
        os.system('chcp 65001 >nul 2>&1')
    if sys.stdout.encoding != 'utf8':
        sys.stdout.reconfigure(encoding='utf8')
    if sys.stderr.encoding != 'utf8':
        sys.stderr.reconfigure(encoding='utf8')
    wifi = Wifi()
    wifi.main()
