from machine import Pin
import time

# définition du capteur ILS
button = Pin(2, Pin.IN)  

mode_pluie = False
temps_fin_pluie = 0
durée_pluie = 10 * 60  # 10 minutes en secondes
compteur_basculements = 0

# anti-rebond 
temps_précédent = 0
nouveau_basculement = False

# interruption (ISR)
def detection_basculement(pin):
    global compteur_basculements, temps_précédent, nouveau_basculement
    temps_actuel = time.ticks_ms()
    
    # filtrage anti-rebond simple (200 ms)
    if time.ticks_diff(temps_actuel, temps_précédent) > 200:
        compteur_basculements += 1
        temps_précédent = temps_actuel
        nouveau_basculement = True  

# activation de l'interruption sur front descendant
button.irq(trigger=Pin.IRQ_FALLING, handler=detection_basculement)

# boucle principale
while True:
    
    if nouveau_basculement:  
        nouveau_basculement = False
        mode_pluie = True
        temps_fin_pluie = time.time() + durée_pluie
        print(f"Mode pluie activé - Basculement n°{compteur_basculements}")
    
    elif mode_pluie and time.time() >= temps_fin_pluie:
        mode_pluie = False
        print("Mode pluie désactivé")
    
    time.sleep(0.01)  # pause pour libérer le CPU