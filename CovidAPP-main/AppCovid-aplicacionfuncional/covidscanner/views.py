from django.shortcuts import render
from .helpers import QRDecoder, enviarCorreos

# Create your views here.

import pyrebase
import cv2
import qrcode as qr
import cv2 
import zlib

import pprint
import pyrebase as py
import threading
import sys
import socket
import pickle
import os
import smtplib, ssl
import getpass

from covidscanner.Forms import ImageForm


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
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

def dashboard(request):
    from .helpers import conteo
    conteo()

    AstraZenecaCount = database.child("CovidApp").child('ConteoVacunas').child('Astra Zeneca').get().val()
    JanssenCount = database.child("CovidApp").child('ConteoVacunas').child('Janssen').get().val()
    ModernaCount = database.child("CovidApp").child('ConteoVacunas').child('Moderna').get().val()
    PfizerCount = database.child("CovidApp").child('ConteoVacunas').child('Pfizer').get().val()

    context = {
        'AstraZenecaCount':AstraZenecaCount, 
        'JanssenCount':JanssenCount, 
        'ModernaCount':ModernaCount, 
        'PfizerCount':PfizerCount, 
    }
    return render(request, 'index.html', context)


def QRScanView(request):
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid(): 
            print("Form was valid")
            name_file = str(form.cleaned_data["passports"])
            print(name_file)
            email =form.cleaned_data["email"]
            enviarCorreos(email)
            form.save()
            
            
            path_passport = str(BASE_DIR)  + '/media/media/passports/' + name_file
            mensaje = QRDecoder(path_passport)
            print("Todo ha salido genial")
        else:
            print("#################")
            print("Form wasnt valid")
    else:
        print("Un get")
        form = ImageForm(request.POST or None, request.FILES or None)

    context = {
            "form":form
        }
    return render(request, "scanView.html", context)




def StatsView(request):
    from .helpers import conteo
    conteo()
    AstraZenecaCount = database.child("CovidApp").child('ConteoVacunas').child('Astra Zeneca').get().val()
    JanssenCount = database.child("CovidApp").child('ConteoVacunas').child('Janssen').get().val()
    ModernaCount = database.child("CovidApp").child('ConteoVacunas').child('Moderna').get().val()
    PfizerCount = database.child("CovidApp").child('ConteoVacunas').child('Pfizer').get().val()

    context = {
        'AstraZenecaCount':AstraZenecaCount, 
        'JanssenCount':JanssenCount, 
        'ModernaCount':ModernaCount, 
        'PfizerCount':PfizerCount, 
    }
    return render(request, "stats.html", context)