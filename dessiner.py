#Auteur : Zheng Qin (20151658)
#Auteur : 
#Date : Nov 13 2022
#
#Ce programme est un logiciel d'édition graphique s'apparentant 
#à une version simplifiée du logiciel Microsoft Paint. 
#Ce logiciel permettra à l'utilisateur de dessiner des rectangles 
#de différentes tailles et différentes couleurs à l'aide de la souris.


couleur = ["#fff", "#000", "#f00", "#ff0", "#0f0", "#00f", "#f0f", "#888"]
#Les couleurs possibles en hexadécimal selon la syntaxe des couleurs du Web.
largeur = 180          #Largeur de la résolution en pixels.
hauteur = 120          #Hauteur de la résolution en pixels.
taille = 12            #Taille d'un côté des carrés de couleur en pixels.
longueurCadre = 1      #Taille de la bordure des carrés de couleur en pixels.
espace = 6             #Distance entre chaque carré de couleur.
nombreCouleur = 8      #Nombre de couleurs choisies.
hauteurMenu = 24       #Hauteur de la barre de menu en pixels.
couleurDefaut = "#fff" #Couleur par défaut de la fenêtre.
tab = []               #Tableau donnant les boutons de la barre de menu.

def bouton(x, y, largeur, hauteur, numbre): #Dessine les carrés de couleur.
    fillRectangle(x, y, largeur, hauteur, couleur[numbre])

def boutonEffacer(x, y): #Dessine le bouton effacer.
    fillRectangle(x, x, taille, taille, couleurDefaut)
    for i in range(x, y):
        setPixel(i, x, "#f00")#Construit diagonale du coin supérieur gauche.    
        setPixel(i, y - 1, "#f00")#Construit diagonale du coin inférieur gauche
        x += 1 #Pour continuer le X.
        y -= 1 #Pour continuer le X. 
        
def clear():#Fonction du bouton effacer pour effacer le contenu de la fenêtre.
    fillRectangle(0, hauteurMenu, largeur, hauteur-hauteurMenu, couleurDefaut)
        
def cadre(x, y, largeur, hauteur): #Construit le cadre autour des carrés.
    fillRectangle(x, y, largeur, hauteur, "#000")
        
        
def fenetre(largeur, hauteur): #Dessiner la fenêtre, barre du menu et boutons.
    i = -1
    longueurBouton = taille + longueurCadre * 2
    distCoins = taille + espace
    #Distance entre 2 coins supérieurs gauches consécutifs.
    setScreenMode(largeur, hauteur) #Établit la résolution de l'écran.
    fillRectangle(0, 0, largeur, hauteur, couleurDefaut) #Dessiner fenêtre.
    fillRectangle(0, 0, largeur, hauteurMenu, "#888") #Dessiner barre du menu.
    for x in range(espace, nombreCouleur * distCoins, distCoins):
        cadre(x - 1, espace - 1, longueurBouton, longueurBouton)
        bouton(x, espace, taille, taille, i)
        i += 1
    boutonEffacer(espace, espace + taille)
#La boucle in range dessine chaque carré du menu et fait appel aux fonctions
#cadre pour tous les cadres et carré pour lui donner la couleur établie. 
    
#La fonction creerBoutons retourne les informations utiles de chaque bouton
#la forme d'un tableau d'enregistrements.
def creerBoutons(couleurs, taille, espace, couleurEffacer): 
    distCoins = taille + espace #Distance entre les coins supérieurs gauches.
    tab = [struct(coin1 = struct(x = distCoins + espace, y = espace),
           coin2 = struct(x = distCoins * 2, y = distCoins),
           couleur = couleurEffacer, #Fond blanc du bouton.
           effacer = True)] #Pour premier élément du tableau, bouton effacer.
    numbre = couleur.index(couleurs[0])
    if numbre == 0:
        tab.extend(tab) #Ajout de l'index 0, qui est bouton effacer.
    else:
        tabFinal = [struct(coin1 = struct(x = espace + \
                                 (numbre + 1) * distCoins, y = espace),
                    coin2 = struct(x = distCoins*(numbre + 2), y = distCoins),
                    couleur = couleurs[0],
                    effacer = False)] #Pour les boutons de couleur.
        tab.extend(tabFinal) #Ajout de l'index suivant, qui est une couleur.
    return tab
    
#Fonction trouverBouton vérifie si une position se retrouve dans l'un des
#carrés de couleur.
def trouverBouton(boutons, position): 
    coin1_x = boutons[1].coin1.x  #Établir les coordonnées des coins supérieur
    coin1_y = boutons[1].coin1.y  #gauche et inférieur droit.
    coin2_x = boutons[1].coin2.x
    coin2_y = boutons[1].coin2.y
    if coin1_x <= position[0] <= coin2_x and coin1_y <= position[1] <= coin2_y\
                            and boutons[1].couleur != "#888":
        return True  #Bouton se retrouve aux coordonnées fournies.
    elif boutons[1].effacer == True:
        return None  #Aucun bouton se trouve aux coordonées fournies.
    
def boutonSouris(x):    #Permet de constamment évaluer le programme lorsque
    while True :        #le bouton principal de la souris n'est pas enfoncé.
        souris = getMouse()
        if souris.button == x:
            return souris
        sleep(0.01)     #Nouvelle évaluation de souris à chaque 0.01 seconde.

#tracerRectangle trace un rectangle selon la position du clic initial et la 
#position de la souris lorsque le bouton est maintenu enfoncé.
def tracerRectangle(souris, largeur, hauteur, debut, couleur):
    if souris.x <= debut[0] and hauteurMenu <= souris.y <= debut[1]:
        fillRectangle(souris.x, souris.y, largeur, hauteur,couleur)
      #Coin supérieur gauche donné par la souris.
    elif souris.x <= debut[0] and souris.y > debut[1]:
        fillRectangle(souris.x, debut[1], largeur, hauteur,couleur)
      #Coin supérieur gauche donné par la souris.x et y du clic initial.
    elif hauteurMenu <= souris.y <= debut[1]:
        fillRectangle(debut[0], souris.y, largeur, hauteur, couleur)
      #Coin supérieur gauche donné par x du clic initial et souris.y.
    elif souris.y > debut[1]:
        fillRectangle(debut[0], debut[1], largeur, hauteur,couleur)
      #Coin supérieur gauche donné par le clic initial seulement. 
    elif souris.x <= debut[0] and souris.y < hauteurMenu:
        hauteur = abs(hauteurMenu - debut[1]) + 1  
        fillRectangle(souris.x, hauteurMenu, largeur, hauteur,couleur)
      #Coin supérieur gauche donné par la souris.x et hauteur du menu, car on
      #ne peut dessiner sur le menu directement.
    else:
        hauteur = abs(hauteurMenu - debut[1]) + 1
        fillRectangle(debut[0], hauteurMenu, largeur, hauteur,couleur)
      #Coin supérieur gauche donné par le x du clic initial et hauteur du menu
      # car on ne peut dessiner sur le menu directement.
        
#Procédure dessinerRectangleFlottant anime le rectangle flottant alors que le
#bouton de la souris de l'utilisateur est enfoncé.        
def dessinerRectangleFlottant(imageOriginale, debut, couleur):
    while True:
        souris = getMouse()    #Évalue la souris.
        largeur = abs(souris.x - debut[0])+1 #Largeur du rectangle flottant.
        hauteur = abs(souris.y - debut[1])+1 #Hauteur du rectangle flottant.
        if souris.button == 1: #Le bouton principal est enfoncé.
            clear()            #On efface tout contenu de la fenêtre de dessin.
            rectangle = struct(coin1 = struct(x = min(souris.x, debut[0]),
                                        y = min(souris.y, debut[1])),
                               coin2 = struct(x = max(souris.x, debut[0]),
                                        y = max(souris.y, debut[1])))
            #Avec rectangle, on établit les coins supérieur gauche et inférieur
            #droit avec min qui donnera toujours coin 1 et max toujours coin 2.
            restaurerImage(imageOriginale, rectangle) #Appel pour paramètres.
            tracerRectangle(souris, largeur, hauteur, debut, couleur)
            #Appel pour dessin.
            sleep(0.01)
        if souris.button == 0: #Aucun bouton n'est appuyé.
            ajouterRectangle(tab, rectangle, couleur) #Modification de tab.
            break
            
#Procédure restaurerImage dessine une section rectangulaire de l'image 
#imageOriginale dans la grille de pixels.           
def restaurerImage(imageOriginale, rectangle):
    tab = imageOriginale #Initialement le tableau retourné par creerBoutons.
    for i in range(len(tab)): #Évalue selon la longueur de la grille de pixels.
        x = tab[i][0]
        y = tab[i][1]
        largeur = tab[i][2]   #Établir les paramètres du rectangle.
        hauteur = tab[i][3]
        couleur = tab[i][4]
        tracerRectangle(x, y, largeur, hauteur, couleur) 
        #Appel au dessin avec nouveaux paramètres.                                            

#Procédure modifiant une section rectangulaire du paramètre image. 
def ajouterRectangle(image, rectangle, couleur):
    tab = image
    coin1_x = rectangle.coin1.x    #Établir les coins supérieur gauche et 
    coin1_y = rectangle.coin1.y    #inférieur droit du rectangle.
    coin2_x = rectangle.coin2.x
    coin2_y = rectangle.coin2.y
    largeur = coin2_x - coin1_x + 1 #Largeur du rectangle.
    hauteur = coin2_y - coin1_y + 1 #Hauteur du rectangle.
    tab.extend([[struct(x = coin2_x, y = coin2_y), largeur, hauteur,\
                 (coin1_x, coin1_y), couleur]]) 
    return tab #Retourne un tableau avec couleur pour pixels du rectangle.

#Procédure attendant le prochain clic de l'utilisateur.
def traiterProchainClic(boutons): 
    couleur = couleurDefaut #Blanc.
    while True:
        souris = getMouse()
        if souris.button == 1: #Si le bouton principal est enfoncé.
            position = (souris.x, souris.y) #Endroit enfoncé.
            couleurs = [getPixel(souris.x, souris.y)]#Couleur endroit enfoncé.
            boutons = creerBoutons(couleurs, taille, espace, couleur)
            #De la barre du menu.
            etat = trouverBouton(boutons, position) 
            #Évalue si le clic a lieu sur un bouton.
            if etat == True: 
                couleur = couleurs[0] #Applique la couleur du carré choisi.
            elif position[0] in range(espace,espace+taille+1) and\
                 position[1] in range(espace,espace+taille+1):
                clear()     #Exécute si le clic a lieu sur le boutton effacer.
                tab.clear() #Efface contenu de la fenêtre.
            elif souris.y in range(hauteurMenu + 1,hauteur): 
                debut = (souris.x, souris.y) #Évalue le clic sur la fenêtre.    
                dessinerRectangleFlottant(tab, debut, couleur) #Appel dessin.
            boutonSouris(0)  
        if souris.button == 0:  #Aucun clic, donc retour à l'évaluation 
            boutonSouris(1)     #continue du programme avec boutonSouris.
    
def dessiner(): #Procédure démarrant l'éditeur graphique.
    fenetre(largeur, hauteur) 
    couleurs = [couleurDefaut]
    boutons = creerBoutons(couleurs, taille, espace, couleur)
    while True:
        traiterProchainClic(boutons)
        

def testDessiner(): #Procédure tests unitaires pour l'ensemble du programme.
                    #Mettre en commentaire pour désactiver.
    #Tests unitaires creerBoutons
    #Cas normal.
    assert creerBoutons(["#0f0"], 12, 6, "#fff") == \
    [struct(coin1=struct(x=24, y=6), coin2=struct(x=36, y=18), 
            couleur='#fff', effacer=True),
     struct(coin1=struct(x=96, y=6), coin2=struct(x=108, y=18), 
            couleur='#0f0', effacer=False)]
    #Cas avec fond différent pour Effacer.
    assert creerBoutons(["#0f0"], 12, 6, "#000") == \
    [struct(coin1=struct(x=24, y=6), coin2=struct(x=36, y=18),
            couleur='#000', effacer=True),
     struct(coin1=struct(x=96, y=6), coin2=struct(x=108, y=18),
            couleur='#0f0', effacer=False)]
    #Cas avec hauteur négative.
    assert creerBoutons(["#0f0"], 12, -6, "#fff") == \
    [struct(coin1=struct(x=0, y=-6), coin2=struct(x=12, y=6),
            couleur='#fff', effacer=True),
    struct(coin1=struct(x=24, y=-6), coin2=struct(x=36, y=6),
           couleur='#0f0', effacer=False)]
    #Cas avec 0,0.
    assert creerBoutons(["#f00"], 0, 0, "#fff") == \
    [struct(coin1=struct(x=0, y=0), coin2=struct(x=0, y=0),
            couleur='#fff', effacer=True),
     struct(coin1=struct(x=0, y=0), coin2=struct(x=0, y=0),
            couleur='#f00', effacer=False)]
    #Cas avec nombres non entiers.  
    assert creerBoutons(["#0f0"], -12.5, -6.5, "#fff") == \
    [struct(coin1=struct(x=-25.5, y=-6.5), coin2=struct(x=-38.0, y=-19.0),
     couleur='#fff', effacer=True), 
     struct(coin1=struct(x=-101.5, y=-6.5),coin2=struct(x=-114.0, y=-19.0),
     couleur='#0f0', effacer=False)]      
    
    #Tests unitaires trouverBouton
    boutons = [struct(coin1 = struct(x = 24, y = 6), 
                      coin2 = struct(x = 36, y = 18), couleur = "#fff", 
                      effacer = True),
               struct(coin1 = struct(x = 60, y = 6), 
                      coin2 = struct(x = 72, y = 18), couleur = "#f00", 
                      effacer = False)]
    assert trouverBouton(boutons, (9, 11)) == None          #Bouton effacer.
    assert trouverBouton(boutons, (63, 11)) == True         #Bouton couleur
    assert trouverBouton(boutons, (163, 10)) == None        #Dans le menu.
    assert trouverBouton(boutons, (90, 63)) == None         #Espace dessin.
    assert trouverBouton(boutons, (12, 16)) == None         #Sur cadre.
    
    #Tests unitaires restaurerImage
    setScreenMode(4,4)
    t ='#f00#f00#000#000\n#f00#f00#000#000\n#000#000#000#000\n#000#000#000#000'
    rectangle = struct(coin1 = struct(x=0, y=0), coin2 = struct(x=1, y=1))
    imageOriginale = [[struct(x = 1, y = 1), 2, 2, (0, 0), '#f00']]
    restaurerImage(imageOriginale, rectangle)
    assert exportScreen() == t
    t ='#f00#f00#f00#000\n#f00#f00#f00#000\n#000#f00#f00#000\n#000#000#000#000'
    rectangle = struct(coin1 = struct(x=0, y=0), coin2 = struct(x=1, y=1))
    imageOriginale = [[struct(x = 2, y = 2), 2, 3, (1, 0), '#f00']]
    restaurerImage(imageOriginale, rectangle)
    assert exportScreen() == t
    t ='#f00#f00#f00#000\n#f00#f00#fff#fff\n#000#f00#fff#fff\n#000#000#fff#fff'
    rectangle = struct(coin1 = struct(x=0, y=0), coin2 = struct(x=1, y=1))
    imageOriginale = [[struct(x = 3, y = 3), 2, 3 , (2, 1), '#fff']]
    restaurerImage(imageOriginale, rectangle)
    assert exportScreen() == t
    t ='#f00#f00#f00#000\n#f00#ff0#ff0#fff\n#000#ff0#ff0#fff\n#000#000#fff#fff'
    rectangle = struct(coin1 = struct(x=0, y=0), coin2 = struct(x=1, y=1))
    imageOriginale = [[struct(x = 2, y = 2), 2, 2, (1, 1), '#ff0']]
    restaurerImage(imageOriginale, rectangle)
    assert exportScreen() == t
    t ='#f00#f00#f00#000\n#f00#ff0#ff0#fff\n#0f0#0f0#ff0#fff\n#0f0#0f0#fff#fff'
    rectangle = struct(coin1 = struct(x=0, y=0), coin2 = struct(x=1, y=1))
    imageOriginale = [[struct(x = 1, y = 4), 2, 2, (0, 2), '#0f0']]
    restaurerImage(imageOriginale, rectangle)
    assert exportScreen() == t
    
    #Tests unitaires ajouterRectangle
    assert ajouterRectangle([["#fff"] * 4] * 3,struct(coin1 = struct(x=1, y=1),
    coin2=struct(x = 2,y = 2)),"#000")== [['#fff', '#fff', '#fff', '#fff'],
    ['#fff', '#fff', '#fff', '#fff'], ['#fff', '#fff', '#fff', '#fff'],
    [struct(x = 2, y = 2), 2, 2, (1, 1), '#000']]
    assert ajouterRectangle([["#fff"] * 4] * 3,struct(coin1 = struct(x=1, y=1),
    coin2=struct(x = 2,y = 3)),"#000")==[['#fff', '#fff', '#fff', '#fff'],
    ['#fff', '#fff', '#fff', '#fff'], ['#fff', '#fff', '#fff', '#fff'], 
    [struct(x = 2, y = 3), 2, 3, (1, 1), '#000']]
    assert ajouterRectangle([["#fff"] * 4] * 3,struct(coin1=struct(x=10, y=10),
    coin2=struct(x = -1, y = -1)),"#000")==[['#fff', '#fff', '#fff', '#fff'],
    ['#fff', '#fff', '#fff', '#fff'], ['#fff', '#fff', '#fff', '#fff'],
    [struct(x = -1, y = -1), -10, -10, (10, 10), '#000']]
    assert ajouterRectangle([["#fff"] * 4] * 3,struct(coin1=struct(x=23, y=33),
    coin2=struct(x = 13, y = 23)),"#000")==[['#fff', '#fff', '#fff', '#fff'],
    ['#fff', '#fff', '#fff', '#fff'], ['#fff', '#fff', '#fff', '#fff'],
    [struct(x = 13, y = 23), -9, -9, (23, 33), '#000']]
    assert ajouterRectangle([["#fff"] * 4] * 3,struct(coin1=struct(x=5, y=5),
    coin2=struct(x = 14, y = 24)),"#000")==[['#fff', '#fff', '#fff', '#fff'],
    ['#fff', '#fff', '#fff', '#fff'], ['#fff', '#fff', '#fff', '#fff'],
    [struct(x = 14, y = 24), 10, 20, (5, 5), '#000']]
    
    
testDessiner()
