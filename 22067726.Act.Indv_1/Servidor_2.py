import threading as th
import sys
import socket as sck
import pickle
import os

class Servidor():
	def __init__(self, host=sck.gethostname(), port = input("Escribe el puerto: ")):
		self.clientes = []
		self.mensajes = []
		print("La ip del servidor es: " + sck.gethostbyname(host))
		self.sock = sck.socket()
		self.sock.bind((str(host), int(port)))
		self.sock.listen(20)
		self.sock.setblocking(False)

		aceptar = th.Thread(target=self.aceptarConex)
		procesar = th.Thread(target=self.procesarConex)

		aceptar.daemon = True
		aceptar.start()
		procesar.daemon = True
		procesar.start()
		
		for thread in th.enumerate():
			print("Hilo: " + thread.name + "\n"
			    + "Proceso PID: "+ str(os.getpid()) + "\n"
			 	+ "Daemon: " + str(thread.daemon) +  "\n")
		print("Hilos totales: " + str((th.activeCount()-1)))

		while True:
			mensaje = input('SALIR = Q\n')
			if mensaje == 'Q':
				print("Hasta luego!")
				print("**** Cerrando Servidor... *****")
				self.sock.close()
				sys.exit()
			else:
				pass

				

	def broadcast(self, mensaje, cliente):
		archivo = open("MessagesLog.txt")
		self.mensajes.append(pickle.loads(mensaje))
		print("Los mensajes actuales: " + str(pickle.loads(mensaje)))
		print("Los mensajes totales: " + str(self.mensajes))
		
		for c in self.clientes:
			try:
				if c != cliente:
					archivo.write
					c.send(mensaje)
			except:
				self.clientes.remove(c)

	def aceptarConex(self):
		while True:
			try:
				conn, addr = self.sock.accept()
				print(f"\nConexion aceptada via {conn}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
				for client in self.clientes: 
					data = pickle.dumps(client.usuario + 'connected')
					self.broadcast(data,client);  
			except:
				pass

	def procesarConex(self):
		
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(1024)
						if data:
							self.broadcast(data,c)
					except:
						pass
	
		




s = Servidor()