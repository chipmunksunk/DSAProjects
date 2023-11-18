import numpy as np
import matplotlib.pyplot as plt
from random import randint
from seaborn import heatmap


def Größer_Null(x):
    return max(0, x)


class character_creation:
    def __init__(self, Name, AT, PA, LeP, INI, TP, RS):
        self.name = Name
        self.attack = AT
        self.parade = PA
        self.lifepoints = LeP
        self.initiative = INI
        self.damage = TP
        self.defense = RS
        self.malus = 0

    def character_values(self):
        return {
            "Name": self.name,
            "Attacke": self.attack,
            "Parade": self.parade,
            "Lebenspunkte": self.lifepoints,
            "Initiative": self.initiative,
            "Schaden": self.damage,
            "Rüstung": self.defense,
            "Erschwernis": self.malus
        }


def exchange_of_blows(attacker_val, defender_val, Wucht, Finte):
    print("Angriff mit Wuchtschlag " + str(Wucht) + " und Finte " + str(Finte))
    AT_Wurf = randint(1, 20)
    print("Attackewurf:" + str(AT_Wurf))

    if attacker_val["Attacke"] - Wucht - Finte >= AT_Wurf or AT_Wurf == 1:
        print("Attacke gelungen")
        PA_Wurf = randint(1, 20)
        print("Paradewurf:" + str(PA_Wurf))

        if defender_val["Parade"] - Finte >= PA_Wurf or PA_Wurf == 1:
            print("pariert")
            print("### Ende Schlagabtausch ###")
            print()

        elif defender_val["Parade"] - Finte < PA_Wurf or PA_Wurf == 20:
            print("Parade misslungen")
            print("Verursachter Schaden:" + str(attacker_val["Schaden"] + Wucht))
            defender_val["Lebenspunkte"] = defender_val["Lebenspunkte"] - Größer_Null(
                attacker_val["Schaden"] + Wucht - defender_val["Rüstung"])
            print(str(defender_val["Name"]) + " hat " + str(defender_val["Lebenspunkte"]) + " Leben")

            if defender_val["Lebenspunkte"] < 0:
                print(str(defender_val["Name"]) + " ist tot")

            print("### Ende Schlagabtausch ###")
            print()

    elif attacker_val["Attacke"] - Wucht - Finte < AT_Wurf or AT_Wurf == 20:
        print("Attacke misslungen")
        print("### Ende Schlagabtausch ###")
        print()


def documented_exchange_of_blows(attacker, defender, Wucht, Finte):
    AT_Wurf = randint(1, 20)

    if attacker["Attacke"] - Wucht - Finte - attacker["Erschwernis"] >= AT_Wurf or AT_Wurf == 1:
        attackbool = True
        attacker["Erschwernis"] = 0
        PA_Wurf = randint(1, 20)

        if defender["Parade"] - Finte - defender["Erschwernis"] >= PA_Wurf or PA_Wurf == 1:
            paradebool = True
            defender["Erschwernis"] = 0
            damage = 0

        elif defender["Parade"] - Finte - defender["Erschwernis"] < PA_Wurf or PA_Wurf == 20:
            paradebool = False
            defender["Erschwernis"] = 0
            damage = attacker["Schaden"] + Wucht - defender["Rüstung"]

    elif attacker["Attacke"] - Wucht - Finte - attacker["Erschwernis"] < AT_Wurf or AT_Wurf == 20:
        attackbool = False
        paradebool = True
        attacker["Erschwernis"] = Wucht + Finte
        damage = 0

    return attackbool, paradebool, damage


##### Ausführbare Abläufe #####
def run1():
    Murgrimm = character_creation("Murgrimm", 15, 10, 40, 20, 10, 4).character_values()
    Alrik = character_creation("Alrik", 12, 12, 30, 20, 8, 2).character_values()

    counter_Kampfrunde = 0
    while Murgrimm["Lebenspunkte"] >= 0 and Alrik["Lebenspunkte"] >= 0:
        counter_Kampfrunde += 1
        exchange_of_blows(Murgrimm, Alrik, randint(0, 5), randint(0, 5))
        exchange_of_blows(Alrik, Murgrimm, randint(0, 5), randint(0, 5))
        print("---Ende Kampfrunde " + str(counter_Kampfrunde) + "---")
        print()


def run2():
    Angreifer = character_creation("Angreifer", 20, 15, 40, 14, 10, 4).character_values()
    Verteidiger = character_creation("Verteidiger", 15, 15, 40, 14, 10, 4).character_values()

    repetitions = 10000

    Wuchtmax = 5
    Fintemax = 5

    AT_prob_array = np.zeros((Wuchtmax, Fintemax))
    PA_prob_array = np.zeros((Wuchtmax, Fintemax))
    Mean_Schaden_array = np.zeros((Wuchtmax, Fintemax))

    for Wucht in range(5):
        for Finte in range(5):

            attack_history = []
            parade_history = []
            damage_history = []

            for i in range(repetitions):
                attack, parade, damage = documented_exchange_of_blows(Angreifer, Verteidiger, Wucht, Finte)
                attack_history.append(attack)
                parade_history.append(parade)
                damage_history.append(damage)

            AT_prob_array[Wucht, Finte] = np.sum(attack_history) * 100 / repetitions
            PA_prob_array[Wucht, Finte] = np.sum(parade_history) * 100 / repetitions
            Mean_Schaden_array[Wucht, Finte] = np.sum(damage_history) / repetitions

    fig, (ax_AT, ax_PA, ax_Schaden) = plt.subplots(1, 3)

    heatmap(AT_prob_array, vmin=0, vmax=100, ax=ax_AT)
    heatmap(PA_prob_array, vmin=0, vmax=100, ax=ax_PA)
    heatmap(Mean_Schaden_array, vmin=0, ax=ax_Schaden)

    ax_AT.set_aspect("equal")
    ax_PA.set_aspect("equal")
    ax_Schaden.set_aspect("equal")

    ax_AT.set_ylabel("Finte")

    ax_AT.set_xlabel("Wucht")
    ax_PA.set_xlabel("Wucht")
    ax_Schaden.set_xlabel("Wucht")

    ax_AT.set_title("AT")
    ax_PA.set_title("PA")
    ax_Schaden.set_title("Schaden")

    plt.show()


run2()

