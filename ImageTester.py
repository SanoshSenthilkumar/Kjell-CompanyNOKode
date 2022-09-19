from picamera import PiCamera
from time import sleep
import cv2
import numpy as np
import os

#Endre lokasjon til preferert mappe
lokasjon = "/home/pi/BilderFraOvervaakningskameraet/"

bildenavn1, bildenavn2 = "bilde1", "bilde2"

bildebane1 = lokasjon + "bilde1.jpg"
bildebane2 = lokasjon + "bilde2.jpg"


def bevegelse(bilde1, bilde2):
    #Lagrer informasjon om bildene
    #hentet fra https://betterprogramming.pub/how-to-measure-image-similarities-in-python-12f1cb2b7281
    bilde1_lest = cv2.imread(bildebane1)
    graa_bilde1 = cv2.cvtColor(bilde1_lest, cv2.COLOR_BGR2GRAY)
    histogram1 = cv2.calcHist([graa_bilde1], [0],
                         None, [256], [0, 256])
    
    bilde2_lest = cv2.imread(bildebane2)
    graa_bilde2 = cv2.cvtColor(bilde2_lest, cv2.COLOR_BGR2GRAY)
    histogram2 = cv2.calcHist([graa_bilde2], [0],
                         None, [256], [0, 256])
    
    #Euclidean distanse mellom bilder
    c1 = 0
    
    i = 0
    
    while i<len(histogram1) and i<len(histogram2):
        c1+=(histogram1[i]-histogram2[i])**2
        i += 1
        
    c1 = c1**(1 / 2)
    
    if c1 > 30000:
        return True
    else:
        return False
    
    


def main():
    #For å gjøre klart kamera
    kamera = PiCamera()

    #For å forhindre at bilder blir lagret med samme navn og blir overskrevet
    indeks = 1

    #En loop for å sjekke bevegelse
    while True:
        bilde1 = kamera.capture(bildebane1)
        sleep(2)
        bilde2 = kamera.capture(bildebane2)

        if bevegelse(bilde1, bilde2):
            kamera.capture(lokasjon + "bevegelsesbilde" + str(indeks) + ".jpeg")
            #for å forhindre at bilder blir overskrevet
            indeks = indeks+1

        os.remove(bildebane1)
        os.remove(bildebane2)

        sleep(0.5)


if __name__ == "__main__":
    main()
