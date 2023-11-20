from random import randint
import numpy as np
from seaborn import heatmap
import matplotlib.pyplot as plt


def Größer_Null(x):
    return max(0, x)


def Sinnesschärfe_roll_Probability(KL, IN1, IN2, KL_rerolls, IN_rerolls, Gewitzt_Punkte):
    Erfolg_history = []
    repeats = 100000

    for n in range(repeats):

        dice_1, dice_2, dice_3 = [randint(1, 20) for i in range(3)]
        verfügbare_KL_rerolls = KL_rerolls
        verfügbare_IN_rerolls = IN_rerolls

        while True:

            while dice_1 > KL and verfügbare_KL_rerolls > 0:
                dice_1 = randint(1, 20)
                verfügbare_KL_rerolls -= 1

            if dice_1 > KL and verfügbare_KL_rerolls == 0:
                Erfolg_history.append(False)
                break
            while Größer_Null(dice_2 - IN1) + Größer_Null(dice_3 - IN2) > Gewitzt_Punkte and verfügbare_IN_rerolls > 0:
                if dice_2 > dice_3:
                    dice_2 = randint(1, 20)
                    verfügbare_IN_rerolls -= 1
                else:
                    dice_3 = randint(1, 20)
                    verfügbare_IN_rerolls -= 1

            if Größer_Null(dice_2 - IN1) + Größer_Null(dice_3 - IN2) > Gewitzt_Punkte and verfügbare_IN_rerolls == 0:
                Erfolg_history.append(False)
                break

            Erfolg_history.append(True)
            break

    return np.sum(Erfolg_history) * 100 / repeats


data_array = np.zeros((20, 20))
Zahl_KL_rerolls = 2
Zahl_IN_rerolls = 2
Zahl_Gewitzt_Punkte = 4

for KL_ind, KL in enumerate(range(1, 20)):
    for IN_ind, IN in enumerate(range(1, 20)):
        data_array[KL_ind, IN_ind] = Sinnesschärfe_roll_Probability(KL, IN, IN, Zahl_KL_rerolls, Zahl_IN_rerolls,
                                                                    Zahl_Gewitzt_Punkte)

heatmap(data_array)
plt.show()