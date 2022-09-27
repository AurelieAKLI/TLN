#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date 14 mai 2022
import itertools
from bs4 import BeautifulSoup
import urllib.request
import os
import re

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
os.makedirs("cach", exist_ok=True)  # pour créer le fichier cach
os.makedirs("in_out", exist_ok=True)  # pour créer le fichier cach
open("wordsFile.txt", "a+")
compteur = 3
total = 5
listePredicatATester = []


# Fonction qui retourne le nom
def getNumPredicat(namePred: str):
    liste2 = []
    with open("numRelation.txt", "r") as f:
        data = f.read()
        data = data.split("\n")  # liste de lignes
        for line in data:
            liste2.append(line.split(";"))

        for idR, nomRelation in liste2:
            if (namePred == nomRelation):
                print("idRelation getNum " + idR)
                return idR


# getNumPredicat("r_lieu") #output 15
# =============================================================================

# cette fonction sert à générer le fichier du mot(Terme) donnée
# stocke le fichier dans le dossier cach
# ajoue les mots recherché ainsi leur identifiant dans le fichier wordsFile.txt
def recherche(mot: str, nomRelation=''):
    terme = mot
    listeListebis = []

    with open("wordsFile.txt", "r") as f:
        data = f.read()
        data = data.split("\n")
        for line in data:
            liste2 = line.split(";")
            if (liste2 != [''] and liste2 != [' ']):
                listeListebis.append(liste2)
        # print(listeListebis)

        for word, idTerme in listeListebis:
            # print(terme+"//"+idTerme)
            if (word == mot):
                # print(idTerme)
                return idTerme

    if len(terme.strip().split(' ')) > 1:  # si le mot est composée = contient d'espace Tour Eiffel
        tab = terme.strip().split(' ')
        terme = tab[0] + '+' + tab[1]

        fileLink = "http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + terme + "&rel="
        page = urllib.request.urlopen(fileLink)

        # parse the html
        soup = BeautifulSoup(page, 'html.parser')

        if (soup.find('warning') != None):
            print("Warning !!! ")
            numRelation = getNumPredicat(nomRelation)
            fileLink = "http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + terme + "&rel=" + numRelation
            page = urllib.request.urlopen(fileLink)
            # parse the html
            soup2 = BeautifulSoup(page, 'html.parser')
            soup = soup2

        # find the first results within table return index
        soup = soup.find('code')

        # convertis le BeautifulSoup en string
        soupStr = str(soup)

        terme = re.sub('\+', ' ', terme)
        print(terme)
        if (soupStr == "None"):
            print("désolé, le mot n'existe pas :(")
        else:
            file = open("cach/" + terme + '.txt', 'w')
            file.write(str(soup))
            print("Le mot " + terme + " a été enregistré avec succès !")
            file.close()

        # récupère l'identifiant du mot, marqeur = idTerme
        idTerme = re.search('eid=\d+', soupStr).group(0)
        idTerme = idTerme.split("=")[1]
        print("id de " + terme + "= " + idTerme)

        with open("wordsFile.txt", 'a') as f:
            f.write(terme + ";" + idTerme + "\n")
            f.close()
        return idTerme;
    else:  # le mot de contient pas d'espace
        fileLink = "http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + terme + "&rel="
        page = urllib.request.urlopen(fileLink)

        # parse the html
        soup = BeautifulSoup(page, 'html.parser')

        # on traite le cas de warning !!

        if (soup.find('warning') != None):
            print("Warning !!! ")
            numRelation = getNumPredicat(nomRelation)
            fileLink = "http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + terme + "&rel=" + numRelation
            page = urllib.request.urlopen(fileLink)
            # parse the html
            soup2 = BeautifulSoup(page, 'html.parser')
            soup = soup2

        # find results within table
        soup = soup.find('code')

        # convertis le BeautifulSoup en string
        soupStr = str(soup)

        if (soupStr == "None"):
            print("désolé, le mot n'existe pas :(")
        else:
            file = open("cach/" + terme + '.txt', 'w')
            file.write(str(soup))
            print("Le mot " + terme + " a été enregistré avec succès !")
            file.close()

        # récupère l'identifiant du mot, marqeur = idTerme
        idTerme = re.search('eid=\d+', soupStr)
        if (idTerme != None):
            idTerme = idTerme.group(0)
            idTerme = idTerme.split("=")[1]

            with open("wordsFile.txt", 'a') as f:
                f.write(terme + ";" + idTerme + "\n")
                f.close()
        else:
            print("Mote est inconnu")
            return -1;

    return idTerme;


# recherche("tigre")
# recherche("dangereux")
# =========================================================================

# Fonction qui prends en entrée un fichier et un id d'une prédicat(relation)
# elle retourne le nom de relation
# rt;rtid;'trname';'trgpname';'rthelp'
def recherchePredicat(fichier, identifiantPredicat):
    with open("cach/" + fichier, 'r') as f:
        data = f.read()  # data = c'est tt le fichier
        index1erOcc = data.find("rthelp")
        soup22 = data[index1erOcc:-1]  # depuis le mot rthelp jusqu'a la fin du fichier
        soup23 = soup22.split("//")  # pour enlever les 2 dernier lignes et on fait un tab qui contient 2 case 0 et 1
        predicat = soup23[0]  # le 1er case qui nous intéresse corresond aux relations rt;
        predicat = predicat.split("\n\n")
        predicat = predicat[1]
        listePredicat = predicat.splitlines()

        if (identifiantPredicat != None):  # pour plus de sécurité
            for x in listePredicat:
                y = x.split(";")
                if y[1] == identifiantPredicat:
                    f.close()
                    return y[2]
        else:
            return None


# print(recherchePredicat("tigre.txt", "20")) #retourne 'r_has_magn'
# =========================================================================

# fonction retournant le nom du noeuds/terme en prenant l'id du noeud en question
# // les noeuds/termes (Entries) : e;eid;'name';type;w;'formated name'
def rechercheNoeuds(fichier, identifiantNoeud):
    with open("cach/" + fichier, 'r') as f:
        data = f.read()
        marqueur = data.find("name'")
        soup22 = data[marqueur:-1]
        soup23 = soup22.split("//")
        noeud = soup23[1]
        noeud = noeud.split("\n\n")
        noeud = noeud[1]

        listeNoeud = noeud.splitlines()

        if (identifiantNoeud != None):  # pour plus de sécurité
            for x in listeNoeud:
                y = x.split(";")
                if y[1] == identifiantNoeud:
                    f.close()
                    return y[2]
        else:
            return None


# print(rechercheNoeuds("dangereux.txt", "259315")) # outPut = 'risquer sa vie'
# =========================================================================

# cette fonction cherche le mot en prendant l'id en param
def rechercheMotWordsFile(id):
    listeListebis = []
    with open("wordsFile.txt", "r") as f:
        data = f.read()
        data = data.split("\n")
        for line in data:
            liste2 = line.split(";")
            if (liste2 != [''] and liste2 != [' ']):
                listeListebis.append(liste2)
        # print(listeListebis)

    for terme, idTerme in listeListebis:
        if (idTerme == id):
            print(terme)
    # return terme


# rechercheMotWordsFile('48510')  #out put: le mot dangereux

# =========================================================================

# r_s : relation sortante            r_e:   relation entrante
# rid_s: id relation sortante        rid_e: id relation entrante
# node1_s: noeud1 sortant            node1_e: noeud intermédiaire
# node2_s: noeud intermédiaire       node2_e: noeud2
# type_s: type de relation           type_e: type de relation
# w_s: poids                         w_e: poids du 2eme relation

def rechercheinference(idTerm1, idTerme2, listeListe, listeListe_bis, fichierS, fichierE, userPredicat):
    compteur = 0
    L = []
    # print(idTerm1,idTerme2,listeListe, listeListe_bis, fichierS, fichierE, userPredicat)
    for (r_s, rid_s, node1_s, node2_s, type_s, w_s) in listeListe:  # liste sortante
        for (r_e, rid_e, node1_e, node2_e, type_e, w_e) in listeListe_bis:  # liste entrante
            # print(node2_s+" - "+node1_e)
            if (node2_s == node1_e) and ((recherchePredicat(fichierS, type_s) == "'" + userPredicat + "'") or (
                    recherchePredicat(fichierE, type_e) == "'" + userPredicat + "'")):
                compteur = compteur + 1
                L.append((node1_s, type_s, node2_s, type_e, node2_e, w_s, w_e))

    print("Il y a ", compteur, " inférences\n")
    return L


# =========================================================================

def inference(mot1: str, mot2: str, relation: str):
    idTerme1 = recherche(mot1, relation)
    idTerme2 = recherche(mot2, relation)

    ################# Pour Terme 1 #######################
    # ici on enléve les poids -ve pour le terme 1
    list1 = []
    with open("cach/" + mot1 + '.txt', 'r') as f:
        data = f.read()
        marqueur = data.find("sortantes")
        marqueurtEntrant = data.find("// les relations entrantes ")
        marqueurEnd = data.find("// END")
        soup22 = data[marqueur:marqueurtEntrant]  # depuis le mot sortantes jusqu'a la fin du fichier
        sortant = soup22.split("\n")

        file = open("in_out/sortantes_" + mot1 + ".txt", 'w')
        for line in sortant:
            if line.find(";-") != -1:
                pass
            else:
                listEle = line.split(";")
                if (len(listEle) == 6):
                    list1.append(listEle)
                file.write(line + "\n")
        print("Le fichier " + mot1 + " entrante a été enregistré avec succès !")
        file.close()

    list1 = list1[2:-1]

    ################# Pour Terme 2 #######################
    # ici on enléve les poids -ve pour le terme 1
    list2 = []
    with open("cach/" + mot2 + '.txt', 'r') as f:
        data = f.read()
        marqueur = data.find("// les relations entrantes")
        marqueurEnd = data.find("// END")
        soup = data[marqueur:marqueurEnd]  # depuis le mot sortantes jusqu'a la fin du fichier
        entrante = soup.split("\n")

        file = open("in_out/entrante_" + mot2 + ".txt", 'w')
        for line in entrante:
            if line.find(";-") != -1:
                pass
            else:
                listEle = line.split(";")
                if (len(listEle) == 6):
                    list2.append(listEle)
                file.write(line + "\n")
        print("Le fichier " + mot2 + " entrante a été enregistré avec succès !")
        file.close()
        list2 = list2[2:-1]

    print("====================================================")
    print("Tu m'as demandé si " + mot1 + " " + relation + " " + mot2 + " ?")
    liste = rechercheinference(idTerme1, idTerme2, list1, list2, mot1 + ".txt", mot2 + ".txt", relation)

    if (liste == []):
        print("il n'y a pas d'infèrence :(")
    else:
        fileRes = open("FileRes", "w")
        lRes = []
        resStr = ""
        print("voici les infèrences trouvées : ")
        for (node1_s, type_s, node2_s, type_e, node2_e, w_s, w_e) in liste:
            n1 = recherchePredicat(mot1 + ".txt", type_s).replace("'", "")
            n2 = rechercheNoeuds(mot1 + ".txt", node2_s).replace("'", "")
            n3 = recherchePredicat(mot2 + ".txt", type_e).replace("'", "")

            resStr += mot1 + ";" + n1 + ";" + n2 + ";" + n3 + ";" + mot2 + "\n"
            lRes.append(resStr)
            fileRes.write(str(resStr))
        # print(lRes) #une liste de tt le text
        resfinal = []
        res = resStr.split("\n")
        for ligne in res:
            l = ligne.split(";")
            if (len(l) == 5):
                resfinal.append(l)
        # print(resfinal)
        print("\n********** Voici les inférences trouvées avant raffinement *********** \n")
        raffinementBis(resfinal)

        print("\n*********** Voici les inférences trouvées après raffinement *********** \n")
        raffinement(resfinal, relation, compteur, total)

        print("Oui, c'est vrai !")


def raffinement(listeRes, relation, compteur, total):
    cpt = 0
    res = list(k for k, _ in itertools.groupby(listeRes))  # pour enlever les duplicats
    for (motX, pred1, motZ, pred2, motY) in res:
        if (pred1 == relation and pred2 in listePredicatATester) or (
                pred2 == relation and pred1 in listePredicatATester):
            compteur -= 1
        else:  # nouveau predicat trouve
            compteur = 3
            if (pred1 == relation):
                listePredicatATester.append(pred2)
            else:
                listePredicatATester.append(pred1)

        if ("&gt" in pred1 or "&gt" in pred2 or "&gt" in motZ):  # r_nom&gt
            pass
        elif (pred1 == 'r_meaning/glose' or pred2 == 'r_meaning/glose'):
            pass
        elif (pred1 == '::&gt' or motZ == '::&gt' or pred2 == '::&gt'):
            pass
        elif (pred1 == 'r_locution' or pred2 == 'r_locution'):
            pass
        elif (pred1 == 'r_meaning/glose' or pred2 == 'r_meaning/glose'):
            pass
        elif (motX == motZ and pred1 == 'r_lemma') or (motZ == motY and pred2 == 'r_lemma'):
            pass
        elif (pred1 == 'saisir&gt' or pred2 == 'saisir&gt'):
            pass
        elif (pred1 == 'boeuf&gt' or pred2 == 'boeuf&gt'):
            pass
        elif (pred1 == 'r_aki' or pred2 == 'r_aki'):
            pass
        elif (compteur <= 0):
            pass
        elif (total < 0):
            pass
        else:
            total -= 1
            compteur = compteur - 1
            cpt += 1
            print(motX + " | " + pred1 + " | " + motZ + " | " + pred2 + " | " + motY)
    print("\nNb d'inférences trouvées = " + str(cpt))


def raffinementBis(listeRes):  # pour afficher les anciens inférences <-- raffinement niveau 1
    cpt = 0
    res = list(k for k, _ in itertools.groupby(listeRes))  # pour enlever les duplicats
    for (motX, pred1, motZ, pred2, motY) in res:
        if (".&gt" in pred1 or ".&gt" in pred2 or ".&gt" in motZ):  # r_nom&gt
            pass
        elif (pred1 == 'r_meaning/glose' or pred2 == 'r_meaning/glose'):
            pass
        elif (pred1 == '::&gt' or motZ == '::&gt' or pred2 == '::&gt'):
            pass
        elif (pred1 == 'r_locution' or pred2 == 'r_locution'):
            pass
        elif (pred1 == 'r_meaning/glose' or pred2 == 'r_meaning/glose'):
            pass
        elif (motX == motZ and pred1 == 'r_lemma') or (motZ == motY and pred2 == 'r_lemma'):
            pass
        elif (pred1 == 'saisir&gt' or pred2 == 'saisir&gt'):
            pass
        elif (pred1 == 'boeuf&gt' or pred2 == 'boeuf&gt'):
            pass
        elif (pred1 == 'r_aki' or pred2 == 'r_aki'):
            pass
        else:
            cpt += 1
            print(motX + " | " + pred1 + " | " + motZ + " | " + pred2 + " | " + motY)
    print("Nb d'inférences trouvées = " + str(cpt))


###################################################


print("Bienvenu 0_0")
terme1 = input("\nEntrez un premier terme :")
terme2 = input("Entrez un second terme :")
relation = input("Nom de relation :")

print("nous traitons votre demande d'inférence......")
print("==============================================")
print("un petit traitement : ")
inference(terme1, terme2, relation)

################ Teste ###################################
# inference("Airbus A380","atterrir","r_agent-1")
# inference("serveuse","apporter","r_agent-1")
# inference("piston","voiture","r_holo")
# inference("pigeon","voler","r_agent-1")
# inference("chat","miauler","r_agent-1")
# inference("pyramide","Egypte","r_lieu")
# inference("Paris", "France", "r_lieu")
# inference("chihuahua", "France", "r_lieu")
# inference("decouper", "poulet", "r_patient")
# inference("chat","souris","r_patient")
# inference("couper", "pain", "r_patient")
# inference("cuire","steak","r_patient")
