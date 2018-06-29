#-*-coding: utf8-*-

'''
	@Author: Daniel Victor Freire Feitosa
	@Version: 1.0.0

	Github: https://github.com/proxyanon/
	Twiiter: @DanielFreire00
	Youtube: Proxy Sec


	Esse script vai na maquina que vai ser visualizada
'''

import socket
from zlib import compress
from os import path
from sys import exit
from platform import system

try:
	from PIL import ImageGrab, Image
	from ctypes import windll
except ImportError:
	print("\n[#] Desculpe somente Rwindows ...\n")
	exit()

ip = '192.168.1.62' # Coloque o seu IP
port = 8291 # Coloque sua porta

class App():

	screen_width = windll.user32.GetSystemMetrics(0) # largura da resolucao ex: 1360
	screen_height = windll.user32.GetSystemMetrics(1) # altura da resolucao ex: 760

	def __init__(self, ip, port, image_name=path.expanduser("~\\AppData\\Local\\Temp\\stream.jpg")):
		self.ip = ip # IP do servidor
		self.port = port # Porta do servidor
		self.image_name = image_name # Path e nome da imagem que vai ser salva como frame

	def getImage(self): # Essa funcao que vai ficar gerando os frames
		image = ImageGrab.grab(bbox=(0, 0, self.screen_width, self.screen_height)) # Tira um print do tamanho do display no caso 1360x768
		resize = image.resize((800, 500), Image.ANTIALIAS) # Faz o resize para 800x600 para facilitar a transmissao no socket
		resize.save(self.image_name, 'JPEG', quality=60, optimize=False, progressive=False) # Salva e dimnui consideralvelmente a qualidade do frame (NESCESSARIO)
		resize.close() # Fecha o frame

	def imageToString(self): # Essa funcao ler o frame para ser transmitido
		self.getImage() # Gera o frame
		handle = open(self.image_name, 'rb') # Faz a leitura no modo binario
		string_img = handle.read() # Leitura
		handle.close() # Fecha o frame

		return string_img # Retorna o frame lido

	def compressString(self): # Essa funcao faz a compressao do frame
		compressed = compress(compress(self.imageToString(), 9)) # Comprimi o frame 2x
		#print("Bytes recebidos: {recv} bytes - {compressed} bytes compressed".format(recv=len(self.imageToString()), compressed=len(compressed))) # Auto-explicativo

		return compressed # Retorna o frame comprimido

	def sendImage(self): # Essa funcao envia o frame para o servidor
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria o socket UDP, mais eficiente nesse caso
		packet = self.compressString() # Frame
		packet_size = len(packet) # Tamanho do frame

		s.sendto("LEN:%i"%(packet_size), (self.ip, self.port)) # Envia o tamanho do frame inicialmente
		data, addr = s.recvfrom(1024) # Recebe a resposta do servidor

		if data == "EXIT": # Se receber EXIT sai do programa
			exit() # Auto-explicativo

		if data == "OK": # Se receber OK faz oque esta abaixo
			#print "Streaming %i bytes"%(packet_size) # Auto-explicativo
			s.sendto(packet, addr) # Envia o frame para o servidor
		else: # Se nao
			s.sendto("FAIL", addr) # Envia um FAIL

app = App(ip, port) # Cria a classe App com o endereco do servidor

while True: # Enquanto estiver tudo certo
	app.sendImage() # Fica enviando os frames
