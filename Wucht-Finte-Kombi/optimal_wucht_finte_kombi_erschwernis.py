import numpy as np


def angriff_einzel_ew(at, pa, dmg, ges, f, w):
    # ges = gesamt manövererschwernis
    if at-ges > 1:
        return 1 / 20 * (at - ges) * (1 - (pa - f) / 20) * (dmg + w)
    else:
        return 1 / 20 * (1 - (pa - f) / 20) * (dmg + w)


def angriff_doppel_ew(at, pa, dmg, f1, w1, f2, w2):
    angriff1_success = 1 / 20 * (at - f1 - w1)
    ges = f2+w2
    ges_erschwernis = f1+w1+f2+w2
    return ((angriff1_success * angriff_einzel_ew(at, pa, dmg, ges, f2, w2) +
            (1 - angriff1_success) * angriff_einzel_ew(at, pa, dmg, ges_erschwernis, f2, w2)) +
            angriff_einzel_ew(at, pa, dmg, f1+w1, f1, w1))


at = 15
pa = 12
dmg = 5
f_max = pa
w_max = at
ges_max = at-1
dmg_array = np.zeros(shape=(f_max, w_max, f_max, w_max))

for f1 in range(0, f_max):
    for w1 in range(0, w_max):
        for f2 in range(0, f_max):
            for w2 in range(0, w_max):
                if f1+w1 > ges_max or f2+w2 > ges_max:
                    continue
                dmg_array[f1, w1, f2, w2] = angriff_doppel_ew(at, pa, dmg, f1, w1, f2, w2)

best_index = np.unravel_index(np.argmax(dmg_array), dmg_array.shape)
print(best_index, dmg_array[best_index])
