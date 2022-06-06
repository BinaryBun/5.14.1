from bs4 import BeautifulSoup
import requests


def main(log, passwd):
	with requests.Session() as sess:  # opening session (cookie MoodleSession dying after request)
		# part 1 (getting logintoken by MoodleSession)
		url = 'https://online.mospolytech.ru/login/index.php'
		session = sess.post(url)

		# get logintoken
		sp = BeautifulSoup(session.text, "html.parser")
		token = sp.find("input", {"name": "logintoken"})["value"]
		first_cook = session.cookies["MoodleSession"]
		
		# part 2 (getting valid MoodleSession)
		data = {"username": log,
				"password": passwd,
				"logintoken": token}  # because new request == new logintoken
		session = sess.post(url, data=data)

		if first_cook == sess.cookies["MoodleSession"]:
			return False
		else:
			return sess.cookies["MoodleSession"]



if __name__ == '__main__':
	login = ""
	password = ""
	print(main(login, password))