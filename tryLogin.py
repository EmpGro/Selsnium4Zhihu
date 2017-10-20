from selenium import webdriver
import time

def login(driver):
    time.sleep(2)
    driver.find_element_by_link_text('登录').click()
    time.sleep(1)
    driver.find_element_by_class_name('signin-switch-password').click()
    time.sleep(1)
    account = driver.find_element_by_name('account')
    password = driver.find_element_by_name('password')
    account.clear()
    password.clear()
    time.sleep(1)
    account.send_keys('account') #换成自己账号
    password.send_keys('password')  #换成自己密码
    time.sleep(5)
    driver.find_element_by_class_name('sign-button submit').click()

def main():
	url = "http://www.zhihu.com"
	driver = webdriver.Edge()
	driver.get(url)
	try:
	 	driver.find_element_by_link_text('登录')
	except Exception as e:
	 	print('已经登录')
	else:
	 	login(driver)

	cookie = driver.get_cookies()
	print(cookie)

if __name__ == '__main__':
	main()