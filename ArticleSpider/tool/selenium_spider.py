# coding: utf-8
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time


if __name__ == "__main__":
    # firefox不加载图片
    firefoxProfile = FirefoxProfile()

    # prefs = {
    #     'profile.managed_default_content_settings_images':2,
    # }
    firefoxProfile.set_preference('permissions.default.image', 2)
    brower = webdriver.Firefox(firefoxProfile)
    brower.get("https://www.oschina.net/blog")
    # time.sleep(5)
    # for i in range(5):
    #     brower.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    #     time.sleep(5)
    print(brower.page_source)
    # print(type(brower.page_source))
    # brower.close()