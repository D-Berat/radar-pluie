from machine import Pin
import time

# définition du capteur ILS
button = Pin(2, Pin.IN)
mode_pluie = False
temps_fin_pluie = 0
durée_pluie = 10 * 60  # 10 minutes en secondes
compteur_basculements = 0

# état précédent du capteur pour détecter les basculements
état_précédent = button.value()

while True:
    état_actuel = button.value()
    
    if état_actuel != état_précédent:  # détection d'un changement d'état (basculement)
        compteur_basculements += 1
        mode_pluie = True
        temps_fin_pluie = time.time() + durée_pluie  # réinitialisation du minuteur
        print(f"Mode pluie activé - Basculement n°{compteur_basculements}")
    
    elif mode_pluie and time.time() >= temps_fin_pluie:  # désactivation après la durée
        mode_pluie = False
        print("Mode pluie désactivé")
    
    état_précédent = état_actuel  # mise à jour de l'état précédent
    time.sleep(0.01)  # pause
