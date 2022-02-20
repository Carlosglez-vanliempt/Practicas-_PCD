

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
fire = py.initialize_app(config)
auth = fire.auth()
ddbb = fire.database()


def conteo():

    qr_list = ddbb.child("CovidApp").get()
    moderna = 0
    janssen = 0
    pfizer = 0
    astra = 0
    
    for qr in qr_list.each(): ##RECORREMOS TODOS LOS QR QUE HAYA EN LA APP
        data = ddbb.child(f'CovidApp/{qr.key()}/-260/1/v/0/ma').get()
        
        if (data.val()) == 'ORG-100031184':
            moderna = moderna +1
            ddbb.child(f'CovidApp/{qr.key()}/-260/1/v/0').update({'ma':'Moderna'})
        if (data.val()) == 'ORG-100001699':
            astra = astra +1
            ddbb.child(f'CovidApp/{qr.key()}/-260/1/v/0').update({'ma':'Astra Zeneca'})
        if (data.val()) == 'ORG-100001417':
            janssen = janssen +1
            ddbb.child(f'CovidApp/{qr.key()}/-260/1/v/0').update({'ma':'Janssen'})
        if (data.val()) == 'ORG-100030215':
            pfizer = pfizer +1
            ddbb.child(f'CovidApp/{qr.key()}/-260/1/v/0').update({'ma':'Pfizer'})
        
        ##validamos los que ya estan dentro del programa para tener el conteo al tope
        if (data.val()) == 'Moderna':
            moderna = moderna +1
        if (data.val()) == 'Astra Zeneca':
            astra = astra +1
        if (data.val()) == 'Janssen':
            janssen = janssen +1
        if (data.val()) == 'Pfizer':
            pfizer = pfizer +1
      
        ddbb.child('CovidApp/ConteoVacunas').set({'Moderna': moderna,'Pfizer': pfizer,'Astra Zeneca': astra,'Janssen':janssen})


def QRDecoder(path_passport):
    mensaje = ""
    try:
        fire = py.initialize_app(config)
        auth = fire.auth()
        ddbb = fire.database()
        qr_ = cv2.imread(path_passport)
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
        print("Error")
        print(e)
        mensaje = "Tu codigo QR no se ha procesado correctamente, por favor intentalo nuevo."
    
    return mensaje
    

def enviarCorreos(destinatario):
    import smtplib, ssl
    import getpass
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    username = "trabajofinalpcd2022@gmail.com"
    password = "pcdcovid"
    asunto= "Covid Pasaporte"
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = asunto
    mensaje["From"] = username
    mensaje["To"] = destinatario
    html = f"""
<html>
<body>
    Hola <i>{destinatario}</i><br>
    Espero que estés <b>muy bien</b>
</body>
</html>
"""
    parte_html = MIMEText(html, "html")
    mensaje.attach(parte_html)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(username, password)
        print("Inicio Sesión")
        server.sendmail(username, destinatario, mensaje.as_string())
        print("Mensaje enviado")