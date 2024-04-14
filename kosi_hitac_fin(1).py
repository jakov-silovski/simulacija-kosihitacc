

import math
import matplotlib.pyplot as plt
import time
import pygame
from sys import exit

def kosi_hitac(v0, theta, dt, n,h):
    """
    Funkcija koja racuna poziciju projektila iz kosog hitca.

    Arguments:
    v0 : float
        Pocetna brzina (m/s)
    theta : float
        Kut ispaljivanja u stupnjevima (°)
    dt : float
        Vremenski interval simulacije (s)
    n : int
        Broj koraka
    h : float
        Visina s koje ispaljujemo (m)

    Returns:
    tuple
        Tuple koji sadrzi dvije liste: x and y coordinates of the trajectory
    """

    # Pretvaramo kut u radijane
    theta = math.radians(theta)

    # Komponente pocetne brzine
    vx0 = v0 * math.cos(theta)
    vy0 = v0 * math.sin(theta)

    # akceleracija sile teže
    g = 9.81  # m/s^2

    # liste u kojima pohranjujemo pozicije projektila
    x_putanja = []
    y_putanja = []
    y=h
    # Racunanje pozicije projektila - bez otpora zraka
    tic=time.time()
    while y>=0:
        toc=time.time()
        t=toc-tic
        x = vx0 * t
        y = h + vy0 * t - 0.5 * g * t**2
        x_putanja.append(x)
        y_putanja.append(y)
        
    return x_putanja, y_putanja

def kosi_hitac_real_time(v0, theta, t):
    """
    Funkcija koja racuna poziciju projektila iz kosog hitca.

    Arguments:
    v0 : float
        Pocetna brzina (m/s)
    theta : float
        Kut ispaljivanja u stupnjevima (°)
    t : float
        vrijeme u kojem racunamo simulaciju (s)

    Returns:
    tuple
        koordinate x,y u vfremenu t nakon ispaljivanja
    """

    # Pretvaramo kut u radijane
    theta = math.radians(theta)

    # Komponente pocetne brzine
    vx0 = v0 * math.cos(theta)
    vy0 = v0 * math.sin(theta)

    # akceleracija sile teže
    g = 9.81  # m/s^2

    # Racunanje pozicije projektila - bez otpora zraka
    
    x = vx0 * t
    y = h + vy0 * t - 0.5 * g * t**2
        
    return x,y

def putanja(pozicije,prije):
    for i in range (len(prije)):
        l = prije[i]
        pygame.draw.lines(surface=sim_obj,color='grey',closed=False, points=l)

    
    pygame.draw.lines(surface=sim_obj,color='black',closed=False, points=pozicije)
    
    return

def toranj (h0, Y):
    pygame.draw.line(surface=sim_obj,color="grey", start_pos=(20,Y-h0*10), end_pos=(20,Y), width=100)

    return 

def domet(Y):
    font = pygame.font.Font('freesansbold.ttf', 10)
    for i in range(0,100,10):
        pygame.draw.line(surface=sim_obj,color="black", start_pos=(i*10,Y), end_pos=(i*10,Y-10), width=5)
        text = font.render(f'{i}', False, 'black','white')
        sim_obj.blit(text, (i*10+5,Y-10))
    return

# Primjer pocetnih parametara
v0 = 20  # Pocetna brzina u m/s
theta = 45  # Kut ispaljivanja
dt = 0.1  # Svakih koliko racunamo poziciju
n = 100  # Broj koraka
h = 10  #Visine s koje ispaljujemo (m)

pygame.init()
fps=30
X=1000;Y=500
fpsclock=pygame.time.Clock()
sim_obj=pygame.display.set_mode((X,Y))
White=(255,255,255)
going=True

y=h
tic=time.time()

x_list=[]
y_list=[]
poz=[(0,Y-h*10)]

prije=[]
sim_state='menu'
poc_uvjeti=''
while going:
    
    if sim_state == 'simulacija':
        sim_obj.fill(White)
        toranj(h,Y)
        domet(Y)
        if len(poz)>1:
            putanja(poz,prije)
        top= pygame.image.load('c:/Users/hrvoj/Downloads/top2.png')
        top=pygame.transform.rotate(top,theta)
        sim_obj.blit(top,(0,Y-h*10-20))
    
        t=time.time()-tic
        x,y=kosi_hitac_real_time(v0, theta, t)
        x=x*10
        y=y*10
        y=(Y-y)
        poz.append((x,y))
        pygame.draw.circle(sim_obj, (255,0,0), (x, y), 2)
        if y>Y:
            prije.append(poz)
            sim_state='menu'
            x_put, y_put = kosi_hitac(v0, theta, dt, n, h)
            plt.plot(x_put,y_put,c='black')
            plt.xlabel("udaljenost [m]")
            plt.ylabel("visina [m]")
            plt.text(x=0, y=max(y_put)/20*3, s= f"početna brzina = {v0} m/s")
            plt.text(x=0,y=max(y_put)/20*2, s=f"početna visina = {h} m")
            plt.text(x=0,y=max(y_put)/20*1, s=f"početni kut = {theta} °")
            plt.grid()
            plt.ylim(0,max(y_put)*1.1)
            plt.show()
    
    elif sim_state=='menu':
        sim_obj.fill((225, 225, 225))
        
        font = pygame.font.SysFont('arial', 40)
        title = font.render('unesi pocetne uvjete (brzina,kut,visina):', True, (0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN: 
                # provjera za brisanje slova
                if event.key == pygame.K_BACKSPACE: 
                    #brise zadnje uneseno slovo
                    poc_uvjeti = poc_uvjeti[:-1] 
                #ako je pritisnuto enter znaci da je gotovo upisivanje
                elif event.key ==pygame.K_RETURN:
                    poc_uvjeti=poc_uvjeti.split(',')
                    v0=int(poc_uvjeti[0])
                    theta=int(poc_uvjeti[1])
                    h=int(poc_uvjeti[2])
                    poz=[(0,Y-h*10)]
                    poc_uvjeti=''
                    sim_state='simulacija'
                    tic=time.time()
                else: #unosi novi znak
                    poc_uvjeti += event.unicode
        sim_obj.blit(title,(10,10))
        title = font.render(poc_uvjeti, True, (0, 0, 0))
        sim_obj.blit(title,(10,100))
    for eve in pygame.event.get():
        if eve.type==pygame.QUIT:
            pygame.quit()
            exit()
    
    pygame.display.update()
    fpsclock.tick(fps)


