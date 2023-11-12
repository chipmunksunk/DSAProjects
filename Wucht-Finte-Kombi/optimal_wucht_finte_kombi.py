import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def Wuchtschlag_Finte_Optimizer(AT_eigen, PA_gegner, Schaden_eigen):
    attack_value = AT_eigen
    parade_value = PA_gegner
    dmg_base = Schaden_eigen

    dice_values_W20 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    dice_values_W6 = np.array([1, 2, 3, 4, 5, 6])

    prob_hit_list = np.zeros((attack_value, attack_value))
    dmg_dealt_list = np.zeros((attack_value, attack_value))

    for finte in range(attack_value):
        for wucht in range(attack_value):
            # compute new AT and PA values
            new_attack_value = attack_value - finte - wucht
            new_parade_value = parade_value - finte
            # print(new_parade_value)
            # print(new_attack_value)

            # compute successful attack prob
            if new_attack_value >= 1:
                prob_attack = min(np.sum(dice_values_W20 <= new_attack_value) / 20, 19 / 20)
            else:
                prob_attack = 0
            # print(prob_attack)

            # compute successful parade prob
            if new_parade_value >= 1:
                prob_parade = np.sum(dice_values_W20 <= new_parade_value) / 20
            else:
                prob_parade = 1 / 20

            # compute final hit prob
            prob_hit = prob_attack * (1 - prob_parade)
            prob_hit_list[finte, wucht] = prob_hit

            dmg_dealt = prob_hit * (dmg_base + wucht)
            dmg_dealt_list[finte, wucht] = dmg_dealt

    # information_array = np.array([range(attack_value), prob_hit_list])
    # information_array = np.array(prob_hit_list)
    np.set_printoptions(precision=2)

    # for prob_hit_row in prob_hit_list:
    #    print(prob_hit_row)

    # print('\n')
    # for dmg_dealt in dmg_dealt_list:
    #    print(dmg_dealt)

    optimal_wucht_finte = np.unravel_index(np.argmax(dmg_dealt_list), dmg_dealt_list.shape)

    # print(optimal_wucht_finte)

    # print("Optimale Ansage: Finte: " + str(optimal_wucht_finte[0]) + " Wucht: " + str(optimal_wucht_finte[1]))
    # print("Mit Trefferwahrscheinlichkeit: " + str(round(prob_hit_list[optimal_wucht_finte[0],optimal_wucht_finte[1]], 2)) )
    # print("Und durschnittlicher Schaden von: " + str(round(dmg_dealt_list[optimal_wucht_finte[0],optimal_wucht_finte[1]], 2)))

    return dmg_dealt_list, optimal_wucht_finte


def ax_plot(x, y_list, ax, x_label, y_label, title, label_list):
    for y, label in zip(y_list, label_list):
        ax.plot(x, y, label=str(label))
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)


fig, ax = plt.subplots(1, 4)

Optimum_Wucht = []
Optimum_Finte = []

AT_Liste = range(1, 40)
PA_Liste = [5,10,15,20]
Schaden_Liste = [5, 10, 15, 20]

for i in range(len(PA_Liste)):
    PA = PA_Liste[i]
    for Schaden in Schaden_Liste:
        Wucht_Liste = []
        Finte_Liste = []
        for AT in AT_Liste:
            Schaden_list, optimale_Ansage = Wuchtschlag_Finte_Optimizer(AT, PA, Schaden)
            Finte_Liste.append(optimale_Ansage[0])
            Wucht_Liste.append(optimale_Ansage[1])
        ax[i].plot(Wucht_Liste, Finte_Liste, label=str(Schaden), marker='s',markersize=Schaden/5, zorder=20-Schaden)
    ax[i].set_xlabel('Wucht')
    ax[i].set_xlim((-1, 20))
    ax[i].set_ylim((-1, 20))
    ax[i].set_title('PA:'+str(PA))

ax[0].set_ylabel('Finte')
plt.legend()
plt.show()
