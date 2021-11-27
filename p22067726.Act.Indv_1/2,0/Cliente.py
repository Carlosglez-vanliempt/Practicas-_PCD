import threading
import sys
import socket
import pickle
import os
import pyrebase

class Cliente():
    host_ = input("Escribe la direccion ip que desee conectarse a: ")
    port_ = int(input("Escribe el puerto con el que desea comunicarse: "))

    nick = input("Nombre de usuario: ")

    nicks = []

    def __init__(self,host=socket.gethostname(), port=port_, nickname=nick):
        self.sock = socket.socket()
        self.sock.connect((str(host), int(port)))
        self.nickname = nickname
        try:
            hilo_recv_mensaje = threading.Thread(target=self.recibir)
            hilo_recv_mensaje.daemon = True
            hilo_recv_mensaje.start()
            print('Hilo con PID', os.getpid())
            print('Hilos activos', threading.active_count())
            self.enviarNick(nickname) #envia el nickname al conectarse por primera vez

            while True:
                msg = input('\nEscriba texto ? ** Enviar = ENTER ** Abandonar Chat = Q \n')
                try:
                    with open("log-22067726.txt", "a+") as Mensajeescribir:
                        Mensajeescribir.write(nickname + ": " + msg + "\n")
                except Exception as e:
                    print("Error de escritura!")
                    print(e)
                if msg != 'Q':
                    self.enviar(nickname + ": " + msg)#funcion para enviar --> nombre: (mensaje)
                else:
                    print(" **** TALOGOOO  ****")
                    self.sock.close()
                    sys.exit()
        except:
            raise Exception

    def recibir(self):
        while True:
            try:
                data = self.sock.recv(32)
                if data:
                    print(pickle.loads(data))
            except:
                pass

    def enviar(self, msg):
        self.sock.send(pickle.dumps(msg))#envia el mensaje al servidor 

    def enviarNick(self, nick_):
        self.sock.send(pickle.dumps(nick_))#envia los nicks al servidor


c = Cliente()
