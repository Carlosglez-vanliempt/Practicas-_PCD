from tkinter import E
from django.test import TestCase

# Create your tests here.
from .helpers import QRDecoder


import pyrebase as py
import pprint
import cv2
from base45 import b45decode
import cbor2
import zlib

config = {
    'apiKey': "AIzaSyByJhZKkc9G0B-MrOOsnuDxIgUUELIEKyM",
  'authDomain': "covid19-e6bf1.firebaseapp.com",
  'databaseURL': "https://covid19-e6bf1-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "covid19-e6bf1",
  'storageBucket': "covid19-e6bf1.appspot.com",
  'messagingSenderId': "96661594726",
  'appId': "1:96661594726:web:d1dcb138c79bf3f4f1c3a7",
  'measurementId': "G-4QXVFPQ3PM"
}




def QRDecoder(passport):
	mensaje = ""
	try:
		fire = py.initialize_app(config)
		auth = fire.auth()
		ddbb = fire.database()
		qr_ = cv2.imread(passport)
		print(qr_)
		detector = cv2.QRCodeDetector()
		text, arr, deci = detector.detectAndDecode(qr_)
		print(text)
		print(arr)
		print(deci)
		data = text
		data = data.replace("HC1:","")
		z_data = b45decode(data)
		databytes = bytes(z_data)
		decompress = zlib.decompress(databytes)
		decode = cbor2.loads(decompress)
		decodedData = cbor2.loads(decode.value[2])
		pprint.pprint(decodedData)
		num_qr = ddbb.child("CovidApp").get()
		lastvalorqr = 0
		for qr in num_qr.each(): ##RECORREMOS TODOS LOS QR QUE HAYA EN LA APP
			lastvalorqr = lastvalorqr + 1
		ddbb.child(f'CovidApp/QR{lastvalorqr}').set(decodedData) ## QR DINAMICO

		print("Fantastico, la funcion ha sido un exito.")
		mensaje = "Tu codigo QR ha sido leido y procesado con éxito."
		
	except Exception as e:
		print("Error en la funcion: ")
		print(e)
		mensaje = "Tu codigo QR no se ha procesado correctamente, por favor intentalo nuevo."


