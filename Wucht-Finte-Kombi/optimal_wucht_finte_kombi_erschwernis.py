import numpy as np


def angriff_einzel_ew(at, pa, dmg, ges, f, w):
    # ges = gesamt manövererschwernis
    if at-ges > 1:
        return 1 / 20 * (at - ges) * (1 - (pa - f) / 20) * (dmg + w)
    else:
        return 0


def angriff_doppel_ew(at, pa, dmg, f1, w1, f2, w2):
    p_AT1 = 1 / 20 * (at - f1 - w1)
    ges = f2+w2
    ges_erschwert = ges + f1 + w1
    return ((p_AT1 * angriff_einzel_ew(at, pa, dmg, ges, f2, w2) +
             (1 - p_AT1) * angriff_einzel_ew(at, pa, dmg, ges_erschwert, f2, w2)) +
            angriff_einzel_ew(at, pa, dmg, f1+w1, f1, w1))


# p_AT1 * (1-p_PA1)  * p2 * t2

# def angriff_doppel_ew_v2(at, pa, dmg, f1, w1, f2, w2):
#     ges2 = f2 + w2
#     ges1 = f1 + w1
#     ges_erschwert = ges2 + ges1
#
#     return (2 * angriff_einzel_ew(at, pa, dmg, ges1, f1, w1) + angriff_einzel_ew(at, pa, dmg, ges2, f2, w2) +
#             angriff_einzel_ew(at, pa, dmg, ges_erschwert, f2, w2))

# def angriff_doppel_ew_v2(at, pa, dmg, f1, w1, f2, w2):
#     p1 = (at - f1 - w1) / 20 * (1 - (pa - f1) / 20)
#     p2 = (at - f2 - w2) / 20 * (1 - (pa - f2) / 20)
#     pd1 = (1 - p1)
#     pd2 = (1 - p2)
#     p2m = (at - f2 - w2 - f1 - w1) / 20 * (1 - (pa - f2) / 20)
#
#     t1 = (dmg + w1)
#     t2 = (dmg + w2)
#
#     return p1 * p2 * (t1 + t2) + p1 * pd2 * t1 + pd1 * p2m * t2



at = 18
pa = 13
dmg = 1
f_max = pa
w_max = at
ges_max = at-1
dmg_array = np.zeros(shape=(f_max, w_max, f_max, w_max))
dmg_array_2 = np.zeros(shape=(f_max, w_max, f_max, w_max))

for f1 in range(0, f_max):
    for w1 in range(0, w_max):
        for f2 in range(0, f_max):
            for w2 in range(0, w_max):
                if f1+w1 > ges_max or f2+w2 > ges_max:
                    continue
                dmg_array[f1, w1, f2, w2] = angriff_doppel_ew(at, pa, dmg, f1, w1, f2, w2)
                dmg_array_2[f1, w1, f2, w2] = angriff_doppel_ew_v2(at, pa, dmg, f1, w1, f2, w2)

                diff = dmg_array[f1, w1, f2, w2] - dmg_array_2[f1, w1, f2, w2]
                print(diff)

# dmg_array = np.zeros(shape=(f_max, w_max))
# for f1 in range(0, f_max):
#     for w1 in range(0, w_max):
#         dmg_array[f1, w1] = angriff_einzel_ew(at, pa, dmg, f1+w1, f1, w1)

# print(angriff_doppel_ew(at, pa, dmg, 3, 2, 3, 4))
# print(angriff_doppel_ew_v2(at, pa, dmg, 3, 2, 3, 4))

best_index = np.unravel_index(np.argmax(dmg_array), dmg_array.shape)
best_index2 = np.unravel_index(np.argmax(dmg_array_2), dmg_array_2.shape)

print(best_index, dmg_array[best_index])
print(best_index2, dmg_array[best_index2])
