from selenium import webdriver
import time
from SleepCountdown.SleepCountdown import sleep_countdown
import pyautogui as pag


SIDRA_URL = "https://sdarot.dev/watch/"

SEASON_DOWNLOAD = 1
START_EP = 1
END_EP = 13

SEASON = "season"
EPISODE = "episode"

UNSAFE_RELOAD_BUTTON_XPATH = '//*[@id="primary-button"]'
PLAY_EP_BUTTON_XPATH = '//*[@id="proceed"]'
PLACE_FOR_ERROR_AND_DOWNLOAD_BUTTON = '//*[@id="loading"]/div/div[2]/a'
VIDEO_XPATH = '//*[@id="videojs_html5_api"]'
SOURCE_VIDEO_XPATH = '/html/body/video'
BIG_BOY_BUTTON_XPATH = '//*[@id="warning"]/section/button'

driver: webdriver


def get_ep_url(se, ep, sidra=SIDRA_URL):
    return f"{sidra}/{SEASON}/{se}/{EPISODE}/{ep}"


def save_video(se, ep):
    pag.hotkey('ctrl', 's')
    time.sleep(2.5)
    pag.write(f'{se}_{ep}', interval=0.15)
    time.sleep(1)
    pag.press('enter')


def main():
    global driver  # so window doesn't close

    driver = webdriver.Chrome()

    for curr_ep in range(START_EP, END_EP+1):
        driver.get(get_ep_url(SEASON_DOWNLOAD, curr_ep))

        sleep_countdown(5)

        # refresh until google say site is safe
        elems = driver.find_elements_by_xpath(UNSAFE_RELOAD_BUTTON_XPATH)
        while len(elems) != 0:
            elems[0].click()
            elems = driver.find_elements_by_xpath(UNSAFE_RELOAD_BUTTON_XPATH)

        time.sleep(5)

        # press I am big boy button
        try:  # if not found can throw exception
            butt = driver.find_element_by_xpath(BIG_BOY_BUTTON_XPATH)
            if butt is not None and butt.is_displayed() and butt.is_enabled():
                butt.click()
        except:  # no button so just continue
            pass

        # wait until button exist
        play_button = driver.find_element_by_xpath(PLAY_EP_BUTTON_XPATH)

        while not (play_button.is_displayed() and play_button.is_enabled()):
            time.sleep(1)

            try:
                err_download = driver.find_element_by_xpath(PLACE_FOR_ERROR_AND_DOWNLOAD_BUTTON)
            except:
                driver.refresh()
                play_button = driver.find_element_by_xpath(PLAY_EP_BUTTON_XPATH)
                continue

            # will be visible on error on when button is ready
            if err_download.is_displayed():
                if play_button.is_displayed() and play_button.is_enabled():
                    break

                driver.refresh()
                play_button = driver.find_element_by_xpath(PLAY_EP_BUTTON_XPATH)

        play_button = driver.find_element_by_xpath(PLAY_EP_BUTTON_XPATH)
        play_button.click()

        video = driver.find_element_by_xpath(VIDEO_XPATH)
        video_url = video.get_property('src')

        driver.get(video_url)

        sleep_countdown(3)

        save_video(SEASON_DOWNLOAD, curr_ep)

        print(f"Downloaded: {SEASON_DOWNLOAD}-{curr_ep}")


if __name__ == '__main__':
    main()
