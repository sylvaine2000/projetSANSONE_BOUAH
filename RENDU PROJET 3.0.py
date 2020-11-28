import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt
import pytz
import statistics
import scipy.stats
from datetime import datetime

#LECTURE CSV ET RECUPERATION DE DONEES

"Etape 1"
import csv

def convertisseur(chemin):
#Exemple de chemin :    'C:\\Users\\user\\Desktop\\TIPE\\tableau\\Frequence1_bis.csv'
# /!\ Bien mettre les double slash et les guillemets. /!\


    #Tableau sera une liste de listes [[t1, acc1], [t2,acc2] ,... , [tn,accn]]
    Tableau = []
    Temps = []

    #ouverture et lecture du fichier csv
    f = open(chemin)
    csv_f = csv.reader(f)

    # row = ligne ==> ça met le tableur dans le tableau sous forme de liste de listes
    for row in csv_f:
        Tableau.append(row)

    f.close

    #on récupère les "sous listes" du Tableau
    n = len(Tableau)
    for i in range(n-1):
        Temps.append(Tableau[i][0])
    return Temps


"Etape 2"
#TRANSFORMER STRING EN LISTE

tableau=convertisseur(r'C:\Users\vboua\OneDrive\Documents\Cours\Informatique\Projet Info\Donnéesprojetinfo.csv')

def transfo1(tableau):
    n=len(tableau)
    trans=[0]*(n-1)
    for i in range(n-1):
        trans[i]=tableau[i].split(';')
    return trans

T=transfo1(tableau)

def transfo2(T):
    n=len(T)
    U=[]
    for i in range(1,n-1):
        x=T[i]
        V=[]
        for j in range(6):
            V.append(float(x[j]))
        U.append(V)
    return U

#A ce stade, on n'a pas extrait le temps.

W=transfo2(T)

#Pour n'avoir qu'une seule liste, faire l'étape suivante.

def conca(liste):
    n=len(liste)
    C=[]
    for i in range(n-1):
        C+=liste[i]
    return C

C=conca(W)

"Etape 3"
#EXTRAIRE LES DONNEES SEPAREMENT (sauf le temps!).

def recupId(C):
    n=len(C)
    Id=[]
    for i in range(0,n-1,6):
        Id.append(C[i])
    return Id

Id=recupId(C)

def recupNoise(C):
    n=len(C)
    Noise=[]
    for i in range(1,n-1,6):
        Noise.append(C[i])
    return Noise

Noise=recupNoise(C)

def recupTemp(C):
    n=len(C)
    Temp=[]
    for i in range(2,n-1,6):
        Temp.append(C[i])
    return Temp

Temp=recupTemp(C)

def recupHumidity(C):
    n=len(C)
    Humidity=[]
    for i in range(3,n-1,6):
        Humidity.append(C[i])
    return Humidity

Humidity=recupHumidity(C)

def recuplum(C):
    n=len(C)
    lum=[]
    for i in range(4,n-1,6):
        lum.append(C[i])
    return lum

lum=recuplum(C)

def recupCO2(C):
    n=len(C)
    CO=[]
    for i in range(5,n,6):
        CO.append(C[i])
    return CO

CO=recupCO2(C)



"Etape 4"
#EXTRAIRE LES DONNES DE TEMPS

def recupTemps1(T):
    n=len(T)
    Temps=[]
    for i in range(1,n-1):
        Temps.append(T[i][6])
    del Temps[-1]
    return Temps

Temps1=recupTemps1(T)

def recupTemps2(T):
    n=len(T)
    B=[]
    for i in range(n):
        B.append(T[i][:-9])
    return B


Temps2=recupTemps2(Temps1)

#A ce stade, on a enlevé la partie "+0200" et les secondes de la date.


"Etape 5"
#fonctions et courbes"
#spécifier un intervalle de temps

def capteur(numero):
    n=len(Id)
    A=[]
    for i in range(n):
        a=Id.index(Id[i])
        if Id[i]==numero:
            A.append(a)
    return len(A)


def affichercourbe(Parametre,numero):
    deb=input('Rentrer la date de début sous la forme [2020-09-11]:')
    fin=input('Rentrer la date de fin sous la forme [2020-09-11]:')
    j=1
    indicedeb=0
    while j<numero:
        indicedeb+=capteur(j)
        j+=1
    indicefin=indicedeb+capteur(numero)
    A=Temps2[indicedeb:indicefin-1]
    B=Parametre[indicedeb:indicefin-1]
    n=len(A)
    Inter=[]
    G=[]
    H=[]
    for i in range(n-1):
        if A[i][:-6]==deb:
            Inter.append(datetime.strptime(A[i], "%Y-%m-%d %H:%M"))
            G.append(B[i])
            H.append(i)
    if deb==fin:
        unite=input("Rentrer le nom du paramètre et son unité :")
        x = np.array(Inter)
        y = np.array(G)
        plt.plot(x, y)
        plt.ylabel(unite)
        plt.show()
    else:
        b=H[-1]
        while A[b][:-6]!=fin:
            Inter.append(datetime.strptime(A[b], "%Y-%m-%d %H:%M"))
            G.append(B[b])
            b+=1
    if deb!=fin:
        for i in range(b,n-1):
            if A[i][:-6]==fin:
                Inter.append(datetime.strptime(A[b], "%Y-%m-%d %H:%M"))
                G.append(B[b])
        unite=input("Rentrer le nom du paramètre et son unité :")
        x = np.array(Inter)
        y = np.array(G)
        plt.plot(x, y)
        plt.ylabel(unite)
        plt.show()

#Affiche courbe avec axe des ordonnées annoté.


"Etape 6"
#min, max, écart-type, moyenne*, variance, médiane, calculer l’indice “humidex”, etc



def courbe_fonction(numero,Parametre,Parametre2=[0]):
    deb=input('Rentrer la date de début sous la forme [2020-09-11]:')
    fin=input('Rentrer la date de fin sous la forme [2020-09-11]:')
    calc=input('Quel paramètre à afficher sur la courbe (sauf humidex) (choix possibles: min,max,ecart_type,moyenne,variance,mediane,humidex,correlation) ?')
    j=1
    indicedeb=0
    while j<numero:
        indicedeb+=capteur(j)
        j+=1
    indicefin=indicedeb+capteur(numero)
    A=Temps2[indicedeb:indicefin-1]
    B=Parametre[indicedeb:indicefin-1]
    if Parametre2==[0]:
        Z=Parametre2*len(A)
    else:
        Z=Parametre2[indicedeb:indicefin-1]
    n=len(A)
    Inter=[]
    G=[]
    H=[]
    I=[]
    for i in range(n-1):
        if A[i][:-6]==deb:
            Inter.append(datetime.strptime(A[i], "%Y-%m-%d %H:%M"))
            G.append(B[i])
            H.append(i)
            I.append(Z[i])
    if deb==fin:
        if calc=='humidex':
            X=Temp[indicedeb:indicefin-1]
            Y=Humidity[indicedeb:indicefin-1]
            C=[]
            D=[]
            for i in range(n-1):
                if A[i][:-6]==deb:
                    C.append(X[i])
                    D.append(Y[i])
            Ta=statistics.mean(C) #T_air
            a=statistics.mean(D) #humidité
            Tr=(((a/100))**((1/8)))*(112+(0.9*Ta))+(0.1*Ta)-112
            print(Ta+0.555*(6.11*(np.exp((5417.7530)*((1/273.15)-(1/((273.15)+Tr)))))-10))
    else:
        b=H[-1]
        while A[b][:-6]!=fin:
            Inter.append(datetime.strptime(A[b], "%Y-%m-%d %H:%M"))
            G.append(B[b])
            I.append(Z[b])
            b+=1
    if deb!=fin:
        for i in range(b,n-1):
            if A[i][:-6]==fin:
                Inter.append(datetime.strptime(A[b], "%Y-%m-%d %H:%M"))
                G.append(B[b])
                I.append(Z[b])
    if calc=='humidex':
        if deb!=fin:
            X=Temp[indicedeb:indicefin-1]
            Y=Humidity[indicedeb:indicefin-1]
            C=[]
            D=[]
            for i in range(n-1):
                if A[i][:-6]==deb:
                    C.append(X[i])
                    H.append(i)
                    D.append(Y[i])
            if deb!=fin:
                b=H[-1]
                while A[b][:-6]!=fin:
                    C.append(X[b])
                    D.append(Y[b])
                    b+=1
            if deb!=fin:
                for i in range(b,n-1):
                    if A[i][:-6]==fin:
                        C.append(X[b])
                        D.append(Y[b])
            Ta=statistics.mean(C) #T_air
            a=statistics.mean(D) #humidité
            Tr=(((a/100))**((1/8)))*(112+(0.9*Ta))+(0.1*Ta)-112
            print(Ta+0.555*(6.11*(np.exp((5417.7530)*((1/273.15)-(1/((273.15)+Tr)))))-10))
    elif calc=='correlation':
        unite=input("Rentrer le nom du paramètre et son unité :")
        var1=G
        var2=I
        x=np.array(Inter)
        y1=np.array(var1)
        y2=np.array(var2)
        plt.plot(x, y1)
        plt.plot(x, y2)
        #plt.plot(x, x, label=scipy.stats.pearsonr(var1, var2)[0])
        #plt.plot(x, x, label=scipy.stats.spearmanr(var1, var2)[0]))
        plt.ylabel(unite)
        plt.legend()
        plt.show()
        print('Corrélation de Pearson:',scipy.stats.pearsonr(var1, var2)[0])
        print('Corrélation de Spearman:',scipy.stats.spearmanr(var1, var2)[0])
        #print('Corrélation de Kendall:',scipy.stats.kendalltau(var1, var2)[0])
    else:
        unite=input("Rentrer le nom du paramètre et son unité :")
        x = np.array(Inter)
        y = np.array(G)
        plt.plot(x, y)
        plt.show()
        if calc=='max':
            plt.title("Maximum")
            plt.axhline(y=max(G))
            plt.ylabel(unite)
        elif calc=='min':
            plt.title("Minimum")
            plt.axhline(y=min(G))
            plt.ylabel(unite)
        elif calc=='ecart_type':
            plt.title("Ecart Type")
            plt.axhline(y=statistics.pstdev(G))
            plt.ylabel(unite)
        elif calc=='moyenne':
            plt.title("Moyenne")
            plt.axhline(y=statistics.mean(G))
            plt.ylabel(unite)
        elif calc=='variance':
            plt.title("Variance")
            plt.axhline(y=statistics.pvariance(G))
            plt.ylabel(unite)
        elif calc=='mediane':
            plt.title("Médiane")
            plt.axhline(y=statistics.median(G))
            plt.ylabel(unite)
        else:
            print('Pas de fonction correspondante, veuillez réessayer')


"Etape 7"
#Calculer l’indice de corrélation entre un couple de variables

def indicecorel(var1,var2):
    print('Corrélation de Pearson :',scipy.stats.pearsonr(var1, var2)[0])
    print('Corrélation de Spearman :',scipy.stats.spearmanr(var1, var2)[0])
    print('Corrélation de Kendall :',scipy.stats.kendalltau(var1, var2)[0])



"Etape 8"
#BUT DU PROJET
#Trouvez- vous des anomalies dans les données, que pouvez-vous en conclure ? Proposez et implémentez un algorithme permettant de relever les anomalies automatiquement et de les montrer sur les courbes.
#On met en place des fonctions qui détectent les anomalies.

def affichercourbe2(Parametre,numero,deb,fin):
    j=1
    indicedeb=0
    while j<numero:
        indicedeb+=capteur(j)
        j+=1
    indicefin=indicedeb+capteur(numero)
    A=Temps2[indicedeb:indicefin-1]
    B=Parametre[indicedeb:indicefin-1]
    n=len(A)
    Inter=[]
    G=[]
    H=[]
    for i in range(n-1):
        if A[i][:-6]==deb:
            Inter.append(datetime.strptime(A[i], "%Y-%m-%d %H:%M"))
            G.append(B[i])
            H.append(i)
    if deb==fin:
        x = np.array(Inter)
        y = np.array(G)
        plt.plot(x, y)
        plt.show()
    else:
        b=H[-1]
        while A[b][:-6]!=fin:
            Inter.append(datetime.strptime(A[b], "%Y-%m-%d %H:%M"))
            G.append(B[b])
            b+=1
    if deb!=fin:
        for i in range(b,n-1):
            if A[i][:-6]==fin:
                Inter.append(datetime.strptime(A[b], "%Y-%m-%d %H:%M"))
                G.append(B[b])
    x = np.array(Inter)
    y = np.array(G)
    plt.plot(x, y)
    plt.show()


def tout_capteur(Parametre):
    deb=input('Rentrer la date de début sous la forme [2020-09-11]:')
    fin=input('Rentrer la date de fin sous la forme [2020-09-11]:')
    a=affichercourbe2(Parametre,1,deb,fin)
    b=affichercourbe2(Parametre,2,deb,fin)
    c=affichercourbe2(Parametre,3,deb,fin)
    d=affichercourbe2(Parametre,4,deb,fin)
    e=affichercourbe2(Parametre,5,deb,fin)

#le capteur 6 correspond à une plage de temps différente on ne peut pas le mettre sur le graphique.

def detec_anomalie(Parametre,numero):
    j=1
    indicedeb=0
    while j<numero:
        indicedeb+=capteur(j)
        j+=1
    indicefin=indicedeb+capteur(numero)
    A=Temps2[indicedeb:indicefin-1]
    B=Parametre[indicedeb:indicefin-1]
    n=len(B)
    Index=[]
    Ano=[]
    for i in range(1,n-1):
        a=B[i]
        b=B[i-1]
        if Parametre==lum:
            if ((a-b)/(b+1**(-100)))>1:
                Index.append(A[i])
                Ano.append(a)
        else:
            if ((a-b)/(b+1**(-100)))>=0.5:
                Index.append(A[i])
                Ano.append(a)
    m=len(Ano)
    F=[]
    for i in range(m-1):
        x=[Index[i],Ano[i]]
        F.append(x)
    G=np.array(F)
    print('Anomalies :', G)
    x=np.array(A)
    y=np.array(B)
    plt.plot(x, y)
    for i in range(m-1):
        plt.axvline(x=Index[i], color='r')
    plt.show()
    
    
    
