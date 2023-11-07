import numpy as np
import matplotlib.pyplot as plt

easy_life = True

if easy_life:
    attack_value = 1
    parade_value = 20

else:
    attack_value = int(input("Geben sie den AT-Wert des Angreifers an: "))
    parade_value = int(input("Geben sie den PA-Wert des Verteidigers an: "))

dice_values_W20 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
dice_values_W6 = np.array([1, 2, 3, 4, 5, 6])

prob_hit_list = []

for finte in range(attack_value):
    new_attack_value = attack_value - finte
    new_parade_value = parade_value - finte

    # print(new_parade_value)
    # print(new_attack_value)
    prob_attack = np.sum(dice_values_W20 <= new_attack_value) / 20
    print(prob_attack)
    if new_parade_value >= 1:
        prob_parade = np.sum(dice_values_W20 <= new_parade_value) / 20
    else:
        prob_parade = 1 / 20

    prob_hit = prob_attack * (1 - prob_parade)
    prob_hit_list.append(prob_hit)

information_array = np.array([range(attack_value), prob_hit_list])

max_prob = np.max(information_array[1, :])
max_index = np.argmax(information_array[1, :])
print("Höchste Trefferwahrscheinlichkeit (" + str(round(max_prob * 100, 2)) + " %) bei Finte " + str(max_index))