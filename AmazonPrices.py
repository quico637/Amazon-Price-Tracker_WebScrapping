from bs4 import BeautifulSoup
import requests
import pandas
import smtplib
import time

def check_url(url):
	while(url.find("amazon") == -1):
		url = input("Hey, I can only keep track of amazon's product at the moment, so please enter a valid amazon product: ")

def check_email(email):
	while(email.find("@") == -1 or (email.find(".com") == -1 and email.find(".es") == -1)):
		email = input("Hey, that is not a valid e-mail address. Please ensure you typed correctly: ")


def enviar_email(precio_cliente, url, email):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()


	server.login('YOUR-EMAIL', 'YOUR-PASSWORD')

	subject = f"El precio ha bajado a {precio_cliente} euros"

	body = f"Mira el enlace que enviaste: {url}"

	msg = f"Subject: {subject}\n\n{body}"

	server.sendmail(
		'YOUR-EMAIL',
		email,
		msg
	)

	print("El mensaje ha sido enviado!")

	server.quit()


def mirar_link():

	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

	url = input("Hey! let me see the amazon link of the product you want to track: ")
	check_url(url)

	precio_cliente = float(input("At what price do you want me to inform you?: "))
	email = input("What e-mail address would you like to receive updates?: ")
	check_email(email)

	html_text = requests.get(url, headers = headers).text

	soup = BeautifulSoup(html_text, 'html.parser')
	nombre = soup.find(id = "productTitle").get_text().strip()

	precio1 = soup.find(class_ = "a-offscreen").get_text()
	precio = precio1[:-1]

	if(precio.find(".")):
		precio = precio[:-3]
		precio = float(precio.replace(".", ""))
	else:
		precio = float(precio.replace(",", "."))

	print("\n")

	if(precio <= precio_cliente):
		enviar_email(precio_cliente, url, email)

	print("\n")

	print(f"Hey, the following product is being trakced: {nombre}")
	print(f"It actually costs: \t{precio1}")
	print(f"\n\n\tI will inform you at your e-mail address when it gets down to {precio_cliente}{precio1[-1:]}")



while(True):
	mirar_link()
	time.sleep(86400)	#Checks once a day