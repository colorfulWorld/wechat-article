# encoding:utf-8
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# 导入第2-4行是为了马上会提到的 显式等待

import time
import datetime

# 在内存创建一个工作簿obj
# 导入模块

from openpyxl import Workbook
wb = Workbook()
ws = wb.active

driver = webdriver.Chrome()
driver.get('https://weixin.sogou.com/')

# Selenium请求网页等待响应受到网速牵制，如果元素未加载全而代码执行过快就会意外报错而终止，解决方式是等待。
wait = WebDriverWait(driver, 10)
input = wait.until(EC.presence_of_element_located((By.NAME, 'query')))
input.send_keys('宠物')
driver.find_element_by_xpath("//input[@class='swz']").click()

num = 0

def get_news():
    global num # 放全局变量是为了给符合条件的文章记序
    time.sleep(1)
    news_lst = driver.find_elements_by_xpath("//li[contains(@id,'sogou_vr_11002601_box')]")
    for news in news_lst:
        # 获取公众号来源
        source = news.find_elements_by_xpath('div[2]/div/a')[0].text
        # print('source:',source)
        # if '宠物' not in source:
        #     continue
        num += 1
        # 获取文章标题
        title = news.find_elements_by_xpath('div[2]/h3/a')[0].text
        # 获取文章发表日期
        date = news.find_elements_by_xpath('div[2]/div/span')[0].text
        # 文章发表的日期如果较近可能会显示“1天前” “12小时前” “30分钟前”
        # 这里可以用`datetime`模块根据时间差求出具体时间
        # 然后解析为`YYYY-MM-DD`格式
        if '前' in date:
            today = datetime.datetime.today()
            if '天' in date:
                delta = datetime.timedelta(days=int(date[0]))
            elif '小时' in date:
                delta = datetime.timedelta(hours=int(date.replace('小时前', ' ')))
            else:
                delta = datetime.timedelta(minutes=int(date.replace('分钟前', ' ')))
            date = str((today - delta).strftime('%Y-%m-%d'))
        date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
        # 获取url
        url = news.find_elements_by_xpath('div[2]/h3/a')[0].get_attribute('href')
        print(num, title, date)
        print(url)
        print('-' * 10)

for i in range(10):
    get_news()
    if i == 9:
        # 如果遍历到第十页则跳出循环不需要点击“下一页”
        break
    driver.find_element_by_id("sogou_next").click()


driver.find_element_by_name('top_login').click()
while True:
    try:
        next_page = driver.find_element_by_id("sogou_next")
        break
    except:
        time.sleep(3)
next_page.click()

while True:
    get_news()
    try:
        driver.find_element_by_id("sogou_next").click()
    except:
        break

# 最后退出浏览器即可
driver.quit()