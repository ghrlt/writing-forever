import os
import sys
import time
import pickle
import random
import requests
import colorama
from termcolor import cprint

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException


colorama.init()
os.system("mode con: cols=130 lines=30")


class InstagramLogin:
	def __init__(self, username, password, proxy, headless):
		self.username = username
		self.password = password
		self.proxy = proxy
		if proxy and not "http" in proxy:
			self.proxy = f"http://{self.proxy}"

		self.cookies_file = f"WritingForever.{self.username}.cookies"

		self.is_logged_in = False
		self.login(headless=headless)

	def login(self, headless):
		# Init chrome
		chrome_opt = Options()
		chrome_opt.add_argument("window-size=920,980")
		if headless: chrome_opt.add_argument("headless")
		if proxy: chrome_opt.add_argument('--proxy-server=' + self.proxy)
		chrome_opt.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36")
		chrome_opt.add_argument('log-level=2')
		chrome_opt.add_experimental_option("excludeSwitches", ["enable-logging"])
		app = webdriver.Chrome("chromedriver.exe", options=chrome_opt) #Folder of chromedriver.exe must be in path or in cwd

		self.app = app

		if self.hasPreviousCookies():
			app.get("https://instagram.com")
			self.loadCookies()
			for cookie in self.cookies:
				app.add_cookie(cookie)

			app.get("https://instagram.com")

			try: app.find_element_by_xpath("/html/body/div[4]/div/div/button[1]")
			except: self.is_logged_in = True

			try:
				notif_btn = app.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]")
				notif_btn.click()
			except:
				pass
		else:
			app = self.app
			app.get("https://instagram.com")

			time.sleep(2)

			try:
				cookie_btn = app.find_element_by_xpath("/html/body/div[4]/div/div/button[1]")
				cookie_btn.click()
				time.sleep(3)
			except:
				cprint("An error occured, unable to accept cookies.. Include the file", "red", end=" ")
				cprint("Writing...Forever.ERRLOG", "white", end=" ")
				cprint("while reporting the error", "red")
				open("Writing...Forever.ERRLOG", "w", encoding="utf8").write(app.page_source)

				input("Press enter to leave.."); os._exit(1)

			username_input = app.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")
			password_input = app.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")

			username_input.send_keys(self.username)
			time.sleep(2)
			password_input.send_keys(self.password)

			time.sleep(2)

			login_btn = app.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button")
			login_btn.click()

			time.sleep(4)

			try:
				accept_cookies = app.find_element_by_xpath("/html/body/div[4]/div/div/button[2]")
				accept_cookies.click()
				time.sleep(2)
			except:
				pass

			try: 
				saveId_btn = app.find_elements_by_css_selector(".sqdOP.L3NKy.y3zKF")[0]
			except: 
				try: err = app.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/p").text
				except: err = "Unknown. Check your username/password!"
				
				cprint(err, "red")

				cprint("Looks like login failed.. Include the file", "red", end=" ")
				cprint("Writing...Forever.ERRLOG", "white", end=" ")
				cprint("while reporting the error", "red")
				open("Writing...Forever.ERRLOG", "w", encoding="utf8").write(app.page_source)
				input("Press enter to leave.."); os._exit(1)

			saveId_btn.click()
			time.sleep(5)

			try:
				notif_btn = app.find_elements_by_css_selector(".aOOlW.HoLwm")[0]
				notif_btn.click()
			except:
				cprint("Unable to decline notifications.. Include the file", "red", end=" ")
				cprint("Writing...Forever.ERRLOG", "white", end=" ")
				cprint("while reporting the error", "red")
				open("Writing...Forever.ERRLOG", "w", encoding="utf8").write(app.page_source)
				input("Press enter to leave.."); os._exit(1)

			self.saveCookies( app.get_cookies() )
			self.app = app

			return True


	def hasPreviousCookies(self):
		if self.cookies_file in os.listdir():
			return True
		return False

	def loadCookies(self):
		with open(self.cookies_file, "rb") as f:
			self.cookies = pickle.load(f)

		return self.cookies

	def saveCookies(self, cookies):
		with open(self.cookies_file, "wb") as f:
			pickle.dump(cookies, f)
		


class WriteForever:
	def __init__(self, app):
		self.app = app.app

		self.base_txt = "Currently writing.. | "

		self.askTarget()

	def askTarget(self):
		# Get inbox list
		self.app.get("https://www.instagram.com/direct/inbox/")
		time.sleep(2)

		### Add option/by default to get more chats member
		temp = self.app.find_elements_by_css_selector(".qF0y9.Igw0E.IwRSH.eGOV_.ui_ht.i0EQd")
		chats = []
		for chat in temp:
			if chat.text:
				chats.append(chat.text)

		chats_id = [chat.find_element_by_xpath(".//ancestor::a").get_attribute('href') for chat in temp]
		del temp

		cprint("Choose the chat where you want to appear as writing:\n", "white")
		col = 80
		for i in range(0, len(chats), 3):
			txt = [f"\t{i+1}) {chats[i]}"]
			if len(chats) > i+2:
				txt.append(f"{i+2}) {chats[i+1]}")
				if len(chats) > i+3:
					txt.append(f"{i+3}) {chats[i+2]}")

			for e in txt:
				cprint(e + str( " "* (int(col/3) - len(e))), "yellow", end="")
			print()

		cprint(">", "white", attrs=["blink"], end=" "); target = int(input())

		self.target = {"name": chats[target+1], "link": chats_id[target-1]}

	def startToFakeWrite(self):
		try:
			target = self.app.find_element_by_xpath('//a[@href="' + self.target['link'] + '"]')
		except:
			target = self.app.find_element_by_xpath('//a[@href="' + self.target['link'].replace("https://www.instagram.com", "") + '"]')
		target.click()

		try:
			input_area = self.app.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
		except:
			input_area = self.app.find_element_by_tag_name("textarea")[0]

		while True:
			txt = ""
			for _ in range(1, random.randint(2,10)):
				txt += chr(random.randrange(97, 97 + 26))
				
			input_area.send_keys(txt)

			print(self.base_txt + txt + " "*(12-len(txt)), end="\r")
			time.sleep( random.randint(2,3) )

			input_area.send_keys(Keys.CONTROL + "a")
			input_area.send_keys("_")

			print(self.base_txt + " "*12, end="\r")
			time.sleep( random.randint(0,1) )




isHeadless = True

if sys.argv[1:]:
	if sys.argv[1] in ["no-headless", "no-h", "notheadless", "view", "nh"]:
		isHeadless = False



cprint(
r"""
 __      __         .__   __   .__                      _____                                                            
/  \    /  \_______ |__|_/  |_ |__|  ____     ____    _/ ____\  ____  _______   ____  ___  __  ____  _______             
\   \/\/   /\_  __ \|  |\   __\|  | /    \   / ___\   \   __\  /  _ \ \_  __ \_/ __ \ \  \/ /_/ __ \ \_  __ \            
 \        /  |  | \/|  | |  |  |  ||   |  \ / /_/  >   |  |   (  <_> ) |  | \/\  ___/  \   / \  ___/  |  | \/            
  \__/\  /   |__|   |__| |__|  |__||___|  / \___  /    |__|    \____/  |__|    \___  >  \_/   \___  > |__|    /\  /\  /\ 
       \/                               \/ /_____/                                 \/             \/          \/  \/  \/  
""", "magenta")

cprint(
r"""
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

""", "cyan")


cprint("Instagram username > ", "white", end=""); username = input()
cprint("Instagram password > ", "white", end=""); password = input()
print()
cprint("Proxy ? (N/y) > ", "white", end=""); proxy = input().lower()
if proxy in ['yes', 'y', 'ye', 'yea', 'oui', 'o']:
	cprint("ip:port > ", "white", end=""); proxy = input()
else:
	proxy = None

app = InstagramLogin(username, password, proxy, headless=isHeadless)

start = int(time.time())

app = WriteForever(app)
try:
	app.startToFakeWrite()
except KeyboardInterrupt:
	pass

uptime = int(time.time()) - start
app.app.quit()

print()
cprint(
r"""
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

""", "cyan")
h = uptime // 3600
m = uptime % 3600 // 60
s = uptime % 3600 % 60
uptime = '{:02d}:{:02d}:{:02d}'.format(h, m, s)

cprint(f"Stopped writing | Uptime: {uptime}")