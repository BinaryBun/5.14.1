from bs4 import BeautifulSoup
import requests

class polykek(object):
	def __init__(self):
		self.token = ""

	def timetable(self, group):
		'''
			Get JSON from rasp.dmami.ru by group
		'''
		url = f"https://rasp.dmami.ru/site/group?group={group}"
		headers = {"referer": "https://rasp.dmami.ru/"}

		content = requests.post(url, headers=headers)
		return content.json()
		
	def get_token(self, login, password):
		'''
			Get valid cookie MoodleSession from online.mospolytech.ru
		'''
		with requests.Session() as sess:  # opening session (cookie MoodleSession dying after request)
			# part 1 (getting logintoken by MoodleSession)
			url = 'https://online.mospolytech.ru/login/index.php'
			session = sess.post(url)

			# get logintoken
			sp = BeautifulSoup(session.text, "html.parser")
			token = sp.find("input", {"name": "logintoken"})["value"]
			first_cook = session.cookies["MoodleSession"]
			
			# part 2 (getting valid MoodleSession)
			data = {"username": login,
					"password": password,
					"logintoken": token}  # because new request == new logintoken
			session = sess.post(url, data=data)

			if first_cook == sess.cookies["MoodleSession"]:
				return "Error: login or password incorrect"
			else:
				self.token = sess.cookies["MoodleSession"]
				return sess.cookies["MoodleSession"]

	def print_token(self):
		# debug method
		if self.token != "":
			return self.token
		else:
			return "Error: tokin is empty"

	def get_courses(self, MoodleSession=""):
		'''
			Get activ courses
			You can set your MoodleSession but not in self.token
		'''
		if MoodleSession == "" and self.token == "":
			return "Error: tokin is empty"
		else:
			data = {}
			MoodleSession = max(MoodleSession, self.token, key=lambda i:len(i))
			url = f"https://online.mospolytech.ru/"
			cookies = {"MoodleSession": MoodleSession}  # valid moodlesession

			content = requests.post(url, cookies=cookies)
			sp = BeautifulSoup(content.text, "html.parser")
			elements = sp.findAll("div", {"class": "column c1"})
			for element in elements:
				data[element.text] = element.find("a")["href"]

			return data

	def get_ads_courses(self, MoodleSession=""):
		'''
			Get courses from main page
		'''
		if MoodleSession == "" and self.token == "":
			return "Error: tokin is empty"
		else:
			data = {}
			MoodleSession = max(MoodleSession, self.token, key=lambda i:len(i))
			url = f"https://online.mospolytech.ru/"
			cookies = {"MoodleSession": MoodleSession}  # valid moodlesession

			content = requests.post(url, cookies=cookies)
			sp = BeautifulSoup(content.text, "html.parser")
			elements = sp.findAll("div", {"data-type": "1"})
			for element in elements:
				course_name = element.find("div", {"class": "clt_course_title_content"}).text.strip()
				data[course_name] = element.find("a")["href"]

			return data

	def get_grades(self, MoodleSession=""):
		'''
			Get list of courses grades 

			!!! "Итоговая оценка за курс" is missing (<span>)
		'''
		if MoodleSession == "" and self.token == "":
			return "Error: tokin is empty"
		else:
			data = {}
			MoodleSession = max(MoodleSession, self.token, key=lambda i:len(i))
			url = f"https://online.mospolytech.ru/grade/report/overview"
			cookies = {"MoodleSession": MoodleSession}  # valid moodlesession

			content = requests.post(url, cookies=cookies)
			sp = BeautifulSoup(content.text, "html.parser")
			elements = sp.find("tbody").findAll("tr", {"class": ""})
			for element in elements:
				course_tag = element.find("a")
				data[course_tag.text.strip()] = course_tag["href"]

			return data

	def get_grades_by_url(self, url, MoodleSession=""):
		'''
			Get list of grades bu course
		'''
		if MoodleSession == "" and self.token == "":
			return "Error: tokin is empty"
		else:
			data = []
			MoodleSession = max(MoodleSession, self.token, key=lambda i:len(i))
			cookies = {"MoodleSession": MoodleSession}  # valid moodlesession

			content = requests.post(url, cookies=cookies)
			sp = BeautifulSoup(content.text, "html.parser")
			elements = sp.find("tbody").findAll("tr")
			for element in elements[1:]:  # elements[0] it`s name of course
				grades_data = element.findAll("td")
				try:
					data.append([element.find("th").find("a").text, grades_data[0].text, grades_data[1].text,
																	grades_data[2].text, grades_data[3].text,
																	grades_data[4].text, grades_data[5].text])
				except AttributeError:
					#print([url, element])  # log
					pass

			return data

