import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

easy_life = True

if easy_life:
    attack_value = 15
    parade_value = 15

else:
    attack_value = int(input("Geben sie den AT-Wert des Angreifers an: "))
    parade_value = int(input("Geben sie den PA-Wert des Verteidigers an: "))

dice_values_W20 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
dice_values_W6 = np.array([1, 2, 3, 4, 5, 6])

dmg_base = 5

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
            prob_attack = min(np.sum(dice_values_W20 <= new_attack_value) / 20, 19/20)
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

for prob_hit_row in prob_hit_list:
    print(prob_hit_row)
    
print('\n')
for dmg_dealt in dmg_dealt_list:
    print(dmg_dealt)

optimal_wucht_finte = np.unravel_index(np.argmax(dmg_dealt_list), dmg_dealt_list.shape)
print(optimal_wucht_finte)

print("Optimale Ansage: Finte: " + str(optimal_wucht_finte[0]) + " Wucht: " + str(optimal_wucht_finte[1]))
print("Mit Trefferwahrscheinlichkeit: " + str(round(prob_hit_list[optimal_wucht_finte[0],optimal_wucht_finte[1]], 2)) )
print("Und durschnittlicher Schaden von: " + str(round(dmg_dealt_list[optimal_wucht_finte[0],optimal_wucht_finte[1]], 2)))

ax = sns.heatmap(dmg_dealt_list)
plt.title('Schaden bei AT:' + str(attack_value) + ' und PA:' + str(parade_value))
plt.xlabel('Wucht')
plt.ylabel('Finte')
plt.show()