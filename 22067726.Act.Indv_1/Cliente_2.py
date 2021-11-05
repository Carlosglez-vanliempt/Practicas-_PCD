import threading as th
import sys
import socket as sck
import pickle
import os

class Cliente():

	def __init__(self, host= input("Escriba la IP del servidor al que quiere conectarse: "), port= input("Escriba el puerto con el qeu desea conectarse: ")):
		self.sock = sck.socket()
		usuario = input('Introduzca su nombre de usuario: ')
		self.sock.connect((str(host), int(port)))
		hiloRecibirMensaje = th.Thread(target=self.recibirMensaje)
		hiloRecibirMensaje.daemon = True
		hiloRecibirMensaje.start()
		
		for thread in th.enumerate():
			print("Hilo: " + thread.name + "\n"
				+ "Proceso PID: "+ str(os.getpid()) + "\n" 
				+ "Daemon: " + str(thread.daemon) +  "\n")
		print("Hilos totales: " + str((th.activeCount()-1)))

		self.enviarMensaje("<" + usuario + "> se ha conectado")
		while True:
			mensaje = input('\nEscriba texto ? ** Enviar = ENTER ** Abandonar Chat = Q \n')
			mensaje = input("\n>>\n")
			if mensaje != 'Q' :
				self.enviarMensaje(usuario + ": " + mensaje)
			else:
				print(" ****Saliendo del chat...****")
				self.sock.close()
				sys.exit()

	def enviarMensaje(self, mensaje):
		self.sock.send(pickle.dumps(mensaje))
		data = pickle.dumps(mensaje)
		if data: 
			print(pickle.loads(data))

	def recibirMensaje(self):
		while True:
			try:
				data = self.sock.recv(1024)
				if data:
					print(pickle.loads(data))
			except:
				pass
	
c = Cliente()
