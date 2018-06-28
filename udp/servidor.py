#-*-coding: utf8-*-

'''
	@Author: Daniel Victor Freire Feitosa
	@Version: 2.0.0

	Github: https://github.com/proxyanon/
	Twiiter: @DanielFreire00
	Youtube: Proxy Sec


	Esse script vai na maquina que vai visualizar
'''

import cv2, socket
from sys import exit, stdout
from zlib import decompress

class SpyOffSec():

	def __init__(self, ip, port, img_name='frame.jpg'):
		self.ip = ip # ip para conexao do socket
		self.port = int(port) # porta para conexao do socket
		self.img_name = img_name # nome do frame

	def decompress_and_save(self, string):
		decompressed = decompress(decompress(decompress(decompress(string))))
		handle = open(self.img_name, 'wb')
		handle.write(decompressed)
		handle.close()

	def run(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self.ip, self.port))
		s.listen(5)

		while True:

			sock, addr = s.accept()
			data = sock.recv(1024)

			if "LEN:" in data:
				packet_size = int(data.split(":")[1])
				sock.send("OK")

				stdout.write("\rRecebendo: {packet_size}".format(packet_size=packet_size))

				img_recv = sock.recv(packet_size)
				self.decompress_and_save(img_recv)

				frame = cv2.imread(self.img_name, 0) # faz a leitura da imagem
				cv2.imshow('SpyOffSec TCP - por Daniel Victor Freire Feitosa', frame)
				key = cv2.waitKey(113)

			else:
				pass


# banner
print(" ______     ______   __  __     ______     ______   ______   ______     ______     ______    ")
print("/\\ \\ ___\\   /\\  == \\ /\\ \\_\\ \\   /\\  __ \\   /\\  ___\\ /\\  ___\\ /\\  ___\\   /\\  ___\\   /\\  ___\\   ")
print("\\ \\___  \\  \\ \\  _-/ \\ \\____ \\  \\ \\ \\/\\ \\  \\ \\  __\\ \\ \\  __\\ \\ \\___  \\  \\ \\  __\\   \\ \\ \\____ ") 
print(" \\/\\_____\\  \\ \\_\\    \\/\\_____\\  \\ \\_____\\  \\ \\_\\    \\ \\_\\    \\/\\_____\\  \\ \\_____\\  \\ \\_____\\") 
print("  \\/_____/   \\/_/     \\/_____/   \\/_____/   \\/_/     \\/_/     \\/_____/   \\/_____/   \\/_____/ \n")

app = SpyOffSec('0.0.0.0', 8291)
print("Escutando tcp://{ip}:{port}\n".format(ip=app.ip, port=app.port))

try:
	while True:
		app.run()
except KeyboardInterrupt:
	print("\nEncerrando transmissao ...\n")
	exit()