import socket
import threading
import sys
import pickle
import os


class Servidor():
	def __init__(self, host=socket.gethostname(), port = input("Escribe el puerto que desea utilizar para el acceso al servidor: ")):
		self.clientes = []
		self.mensajes = []
		print("La ip del servidor es: " + socket.gethostbyname(host))
		self.sock = socket.socket()
		self.sock.bind((str(host), int(port)))
		self.sock.listen(20)
		self.sock.setblocking(False)

		aceptar = threading.Thread(target=self.aceptarC)
		procesar = threading.Thread(target=self.procesarC)


		aceptar.daemon = True
		aceptar.start()

		procesar.daemon = True
		procesar.start()

		
		for thread in threading.enumerate():
			print("Hilo: " + thread.name + "\n"
				+ "Proceso PID: "+ str(os.getpid()) + "\n"
				+ "Daemon: " + str(thread.daemon) +  "\n")
		print("Hilos totales: " + str((threading.activeCount()-1)))

		while True:
			msg = input('SALIR = Q\n')
			if msg == 'Q':
				print("**** CERRANDO SERVIDOR... *****")
				self.sock.close()
				sys.exit()
			else:
				pass

				

	def broadcast(self, msg, cliente):
		archivo = open("MessagesLog.txt")
		self.mensajes.append(pickle.loads(msg))
		print("Los mensajes actuales: " + str(pickle.loads(msg)))
		print("Los mensajes totales: " + str(self.mensajes))
		
		for c in self.clientes:
			try:
				if c != cliente:
					archivo.write(str(msg))
					c.send(msg)
					archivo.close()
			except:
				self.clientes.remove(c)

	def aceptarC(self):
		while True:
			try:
				conn, addr = self.sock.accept()
				print(f"\nConexion aceptada via {conn}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
				for client in self.clientes: 
					data = pickle.dumps(client.username + 'connected')
					self.broadcast(data,c);  
			except:
				pass

	def procesarC(self):
		
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