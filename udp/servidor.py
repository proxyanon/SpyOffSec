#-*-coding: utf8-*-

'''
	@Author: Daniel Victor Freire Feitosa
	@Version: 1.1.0

	Github: https://github.com/proxyanon/
	Twiiter: @DanielFreire00
	Youtube: Proxy Sec


	Esse script vai na maquina que vai visualizar
'''

import cv2, socket
from zlib import decompress
from sys import exit, stdout
from platform import system

class App():

	def __init__(self, ip, port, image_name='frame.jpg'):
		self.ip = ip # IP para o servidor
		self.port = port # Porta para o servidor
		self.image_name = image_name # Nome qualquer para o frame

	def decompressStringAndSave(self, string_image): # Essa funcao extrai e salva o frame em um imagem
		decompressed = decompress(decompress(string_image)) # Extrai o frame
		handle = open(self.image_name, 'wb') # Abri a imagem no modo binario
		handle.write(decompressed) # Escreve o frame extraido
		handle.close() # Fecha o frame salvo

	def run(self): # Essa eh a funcao principal
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria o socket UDP
		s.bind((self.ip, self.port)) # Inicia o servidor

		while True:
			data, addr = s.recvfrom(1024) # Recebe o tamanho do frame

			if "LEN:" in data: # Se for o tamanho
				packet_size = int(data.split(":")[1]) # Pega o tamanho do frame no formato enviado do cliente
				s.sendto("OK", addr) # Envia um OK para poder receber o frame

				data_, addr_ = s.recvfrom(packet_size) # Recebe o frame
				string_image = data_ # Frame

				stdout.write("\rTrasmitindo ....: {nbytes} bytes".format(nbytes=len(data_)))

				if string_image == "FAIL": break # Se receber um FAIL sai do loop
			else: # Se nao for o tamanho
				s.sendto("FAIL", addr) # Envia um FAIL e sai do loop
				break

			self.decompressStringAndSave(string_image) # Extrai e salva o frame em um imagem
			image = cv2.imread(self.image_name, 0) # Ler o frame com o opencv
			cv2.imshow('SpyOffSec UDP - por Daniel Victor Freire Feitosa', image) # Mostra o frame

			key = cv2.waitKey(113) # Espeara a entrada da tecla q
			if key == 113: # Se for entrada a q
				s.sendto("EXIT", addr_) # Envia um EXIT para o cliente
				s.close() # Fecha o socket
				break # Sai do loop
		cv2.destroyAllWindows() # Destroi as janelas do opencv
		exit() # Sai do programa


# banner
print(" ______     ______   __  __     ______     ______   ______   ______     ______     ______    ")
print("/\\ \\ ___\\   /\\  == \\ /\\ \\_\\ \\   /\\  __ \\   /\\  ___\\ /\\  ___\\ /\\  ___\\   /\\  ___\\   /\\  ___\\   ")
print("\\ \\___  \\  \\ \\  _-/ \\ \\____ \\  \\ \\ \\/\\ \\  \\ \\  __\\ \\ \\  __\\ \\ \\___  \\  \\ \\  __\\   \\ \\ \\____ ") 
print(" \\/\\_____\\  \\ \\_\\    \\/\\_____\\  \\ \\_____\\  \\ \\_\\    \\ \\_\\    \\/\\_____\\  \\ \\_____\\  \\ \\_____\\") 
print("  \\/_____/   \\/_/     \\/_____/   \\/_____/   \\/_/     \\/_/     \\/_____/   \\/_____/   \\/_____/     by @DanielFreire00\n")
                                                                                             

if system() != 'Windows':
	print("[#] Provalvemente este programa nao vai rodar perfeitamente no {plataforma} ...\n".format(plataforma=system()))

app = App('192.168.1.62', 8291) # Cria a classe App com as configuracoes do servidor
print("Escutando: udp://{ip}:{port}\n".format(ip=app.ip, port=app.port)) # auto-explicativo

try:
	while True: # Enquanto estiver tudo certo
		app.run() # Vai receber e mostrar os frames
except KeyboardInterrupt:
	print("\nEncerrando transmissao ...\n")
	exit()
