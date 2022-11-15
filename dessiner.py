#Auteur : #Zheng Qin (20151658)
#Auteur : 
#Date : Nov 13 2022
#
#Ce programme est un logiciel d'édition graphique s'apparentant 
#à une version simplifiée du logiciel Microsoft Paint. 
#Ce logiciel permettra à l'utilisateur de dessiner des rectangles 
#de différentes tailles et différentes couleurs à l'aide de la souris.


#Ce sont des variables globales pour une modification facile
couleur = ["#fff", "#000", "#f00", "#ff0", "#0f0", "#00f", "#f0f", "#888"]
largeur = 180
hauteur = 120
taille = 12
longueurCadre = 1
espace = 6
nombreCouleur = 8
hauteurMenu = 24
couleurDefaut = "#fff"
tab = []

def bouton(x, y, largeur, hauteur, numbre):
    fillRectangle(x, y, largeur, hauteur, couleur[numbre])
    
def boutonEffacer(x, y):
    fillRectangle(x, x, taille, taille, couleurDefaut)
    for i in range(x, y):
        setPixel(i, x, "#f00")
        setPixel(i, y - 1, "#f00")
        x += 1
        y -= 1

def clear():
    fillRectangle(0, hauteurMenu, largeur, hauteur-hauteurMenu, couleurDefaut)
        
def cadre(x, y, largeur, hauteur):
    fillRectangle(x, y, largeur, hauteur, "#000")
        
        
def fenetre(largeur, hauteur):
    i = -1
    longueurBouton = taille + longueurCadre * 2
    distCoins = taille + espace
    setScreenMode(largeur, hauteur)
    fillRectangle(0, 0, largeur, hauteur, couleurDefaut)
    fillRectangle(0, 0, largeur, hauteurMenu, "#888")
    for x in range(espace, nombreCouleur * distCoins, distCoins):
        cadre(x - 1, espace - 1, longueurBouton, longueurBouton)
        bouton(x, espace, taille, taille, i)
        i += 1
    boutonEffacer(espace, espace + taille)
    
    
def creerBoutons(couleurs, taille, espace, couleurEffacer):
    distCoins = taille + espace
    tab = [struct(coin1 = struct(x = distCoins + espace, y = espace),
           coin2 = struct(x = distCoins * 2, y = distCoins),
           couleur = couleurEffacer,
           effacer = True)]
    numbre = couleur.index(couleurs[0])
    if numbre == 0:
        tab.extend(tab)
    else:
        tabFinal = [struct(coin1 = struct(x = espace + \
                                 (numbre + 1) * distCoins, y = espace),
                    coin2 = struct(x = distCoins*(numbre + 2), y = distCoins),
                    couleur = couleurs[0],
                    effacer = False)]
        tab.extend(tabFinal)
    return tab
    

def trouverBouton(boutons, position):
    coin1_x = boutons[1].coin1.x
    coin1_y = boutons[1].coin1.y
    coin2_x = boutons[1].coin2.x
    coin2_y = boutons[1].coin2.y
    if coin1_x <= position[0] <= coin2_x and coin1_y <= position[1] <= coin2_y\
                            and boutons[1].couleur != "#888":
        return True
    elif boutons[1].effacer == True:
        return None
    
def boutonSouris(x):
    while True :
        souris = getMouse()
        if souris.button == x:
            return souris
        sleep(0.01)
         
def tracerRectangle(souris, largeur, hauteur, debut, couleur):
    if souris.x <= debut[0] and hauteurMenu <= souris.y <= debut[1]:
        fillRectangle(souris.x, souris.y, largeur, hauteur,couleur)
    elif souris.x <= debut[0] and souris.y > debut[1]:
        fillRectangle(souris.x, debut[1], largeur, hauteur,couleur)
    elif hauteurMenu <= souris.y <= debut[1]:
        fillRectangle(debut[0], souris.y, largeur, hauteur, couleur)
    elif souris.y > debut[1]:
        fillRectangle(debut[0], debut[1], largeur, hauteur,couleur)
    elif souris.x <= debut[0] and souris.y < hauteurMenu:
        hauteur = abs(hauteurMenu - debut[1]) + 1
        fillRectangle(souris.x, hauteurMenu, largeur, hauteur,couleur)
    else:
        hauteur = abs(hauteurMenu - debut[1]) + 1
        fillRectangle(debut[0], hauteurMenu, largeur, hauteur,couleur)
        

def dessinerRectangleFlottant(imageOriginale, debut, couleur):
    while True:
        souris = getMouse()
        largeur = abs(souris.x - debut[0])+1
        hauteur = abs(souris.y - debut[1])+1
        if souris.button == 1:
            clear()
            rectangle = struct(coin1 = struct(x = min(souris.x, debut[0]),
                                        y = min(souris.y, debut[1])),
                               coin2 = struct(x = max(souris.x, debut[0]),
                                        y = max(souris.y, debut[1])))
            restaurerImage(imageOriginale, rectangle)
            tracerRectangle(souris, largeur, hauteur, debut, couleur)
            sleep(0.01)
        if souris.button == 0:
            ajouterRectangle(tab, rectangle, couleur)
            break
            
            
def restaurerImage(imageOriginale, rectangle):
    tab = imageOriginale
    for i in range(len(tab)):
        x = tab[i][0]
        y = tab[i][1]
        largeur = tab[i][2]
        hauteur = tab[i][3]
        couleur = tab[i][4]
        tracerRectangle(x, y, largeur, hauteur, couleur)

    
def ajouterRectangle(image, rectangle, couleur):
    tab = image
    coin1_x = rectangle.coin1.x
    coin1_y = rectangle.coin1.y 
    coin2_x = rectangle.coin2.x
    coin2_y = rectangle.coin2.y
    largeur = coin2_x - coin1_x + 1
    hauteur = coin2_y - coin1_y + 1
    tab.extend([[struct(x = coin2_x, y = coin2_y), largeur, hauteur,\
                 (coin1_x, coin1_y), couleur]])
    return tab

def traiterProchainClic(boutons):
    couleur = couleurDefaut
    while True:
        souris = getMouse()
        if souris.button == 1:
            position = (souris.x, souris.y)
            couleurs = [getPixel(souris.x, souris.y)]
            boutons = creerBoutons(couleurs, taille, espace, couleur)
            etat = trouverBouton(boutons, position)
            if etat == True:
                couleur = couleurs[0]
            elif position[0] in range(espace,espace+taille+1) and\
                 position[1] in range(espace,espace+taille+1):
                clear()
                tab.clear()
            elif souris.y in range(hauteurMenu + 1,hauteur):
                debut = (souris.x, souris.y)
                dessinerRectangleFlottant(tab, debut, couleur)
            boutonSouris(0)  
        if souris.button == 0:   
            boutonSouris(1)
    

def dessiner():
    fenetre(largeur, hauteur)
    couleurs = [couleurDefaut]
    boutons = creerBoutons(couleurs, taille, espace, couleur)
    while True:
        traiterProchainClic(boutons)
