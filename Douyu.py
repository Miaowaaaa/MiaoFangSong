# coding=utf-8
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import json
import os
import sys
import Utf8

class Douyu:
    def __init__(self,G=False,username=u'',password=''):
        if G:
            self.browser = webdriver.Chrome()
        else:
            _chrome_options = webdriver.ChromeOptions()
            _chrome_options.add_argument('--headless')
            self.browser = webdriver.Chrome(chrome_options=_chrome_options)
        self.username = username
        self.password = password
    def _login(self):

        if os.path.exists('./cookie.json'):
            self.infoCookie()
        else:
            self.infoUserPass()

    def infoUserPass(self):
        self.browser.get("https://www.douyu.com/directory/myFollow")
        while (True):
            time.sleep(2)
            self.browser.find_element_by_xpath("//*[@class='FollowGuest-wrapper']/button").click()
            time.sleep(3)
            #切换到密码登录frame
            self.browser.switch_to.frame("login-passport-frame")
            time.sleep(5)
            #点击密码登录
            self.browser.find_element_by_xpath("//*[@id='loginbox']/div[2]/div[2]/div[3]/div/span[2]").click()
            time.sleep(3)
            #点击QQ图标
            self.browser.find_element_by_xpath("//*[@id='loginbox']/div[3]/div[2]/div[2]/div[2]/a[1]").click()
            time.sleep(3)
            # 获取当前窗口句柄（窗口A）
            handle = self.browser.current_window_handle
            print(handle)
            # 获取当前所有窗口句柄（窗口A、B）
            handles = self.browser.window_handles
            # 对窗口进行遍历
            for newhandle in handles:
                # 筛选新打开的窗口B
                if newhandle != handle:
                    # 切换到新打开的窗口B
                    self.browser.switch_to_window(newhandle)
                    # 在新打开的窗口B中操作
                    self.browser.switch_to.frame("ptlogin_iframe")
                    time.sleep(3)
                    ele = self.browser.find_element_by_id("switcher_plogin").click()
            time.sleep(3)
            self.browser.find_element_by_xpath("//*[@id='u']").send_keys("qq_account")
            time.sleep(3)
            self.browser.find_element_by_xpath("//*[@id='p']").send_keys("qq_password")
            self.browser.find_element_by_xpath("//*[@id='login_button']").click()
            time.sleep(5)
            while (True):
                if 'PHPSESSID' in str(self.browser.get_cookies()):
                    print 'login success'
                    _cookie = self.browser.get_cookies()
                    self._keepCookie(_cookie)
                    break
                else:
                    print 'login fatal'
                    break
            break

    def _keepCookie(self, cookies):
        print 'keeping cookie'
        fp = open('cookie.json', 'w')
        json.dump(cookies, fp)
        fp.close()

    def infoCookie(self):
        print 'exists cookie , loading ... '
        fp = open('cookie.json', 'r')
        cookies = json.load(fp)
        fp.close()
        self.browser.get("https://www.douyu.com")
        for cookie in cookies:
            self.browser.add_cookie(cookie)
        time.sleep(0.5)
        self.browser.refresh()
        if 'acf_nickname' in str(self.browser.get_cookies()):
            print 'login success'

    def _switchRoom(self,rooms,num=1):
        for room in rooms:
            self.browser.get("https://www.douyu.com/"+str(room))
            D._send(num)

    def _send(self,num):
        i = 1
        text = raw_input("input text : ")
        while (i<=num):
            try:
                self.browser.find_element_by_class_name("ChatSend-txt").click()
                # print text.encode('unicode_escape').decode('unicode_escape')
                # continue
                self.browser.find_element_by_class_name("ChatSend-txt").send_keys('No.'+str(i)+' : '+text.encode('unicode_escape').decode('unicode_escape'))
                mouse_ele = self.browser.find_element_by_class_name("ChatSend-button")
                sleep_time = self.browser.find_element_by_class_name("ChatSend-button").text
                # print 'sleep_time ' + str(sleep_time)
                if str.isalnum(str(sleep_time)):
                    st = int(sleep_time)
                else:
                    st = 1
                ActionChains(self.browser).move_to_element(mouse_ele).perform()
                print 'sending data : ' + 'No.'+str(i)+' : '+text.encode('unicode_escape').decode('unicode_escape')
                print u'系统休眠 ' + str(st)
                time.sleep(st)
                mouse_ele.click()
                print ' ok '
                # time.sleep(1)
            except Exception, e:
                print str(e)
            i = i + 1


if __name__ == '__main__':
    username = u''
    password = ''
    D = Douyu(G=True,username=username,password=password)
    D._login()
    rooms = ['71771']
    D._switchRoom(rooms,num=100)

    # testcookie()
    print 'byby'
    D.browser.close()