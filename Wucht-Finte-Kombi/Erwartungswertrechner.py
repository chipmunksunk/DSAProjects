import numpy as np


def create_hit_history_list(num_attacks):
    hit_history_list = ["T", "D"]
    for attacks in range(num_attacks - 1):
        new_hit_history_list = []
        for hit_history in hit_history_list:
            new_hit_history_list.append(hit_history + "T")
            new_hit_history_list.append(hit_history + "D")
        hit_history_list = new_hit_history_list
    return hit_history_list


def prob_normal(AT, PA, wucht, finte):
    return (AT - wucht - finte) / 20 * (1 - (PA - finte) / 20)


def prob_malus(AT, PA, wucht, finte, malus):
    return (AT - wucht - finte - malus) / 20 * (1 - (PA - finte) / 20)


def Erwartungswert(AT, PA, dmg, finte_liste, wucht_liste, num_attacks):
    hit_history_list = create_hit_history_list(num_attacks)
    einzel_erwartungswert_list = []
    finte_liste = list(finte_liste)
    wucht_liste = list(wucht_liste)
    finte_liste.insert(0, 0)
    wucht_liste.insert(0, 0)

    for hit_history in hit_history_list:
        hit_history = "T" + hit_history
        hit_prob_list = []
        damage_list = []
        for i in range(len(hit_history) - 1):

            previous_hit_bool = hit_history[i]
            current_hit_bool = hit_history[i + 1]
            wuchtans = wucht_liste[i + 1]
            finteans = finte_liste[i + 1]
            malusval = wucht_liste[i] + finte_liste[i]
            AT_norm_bool = wuchtans + finteans <= AT - 1
            AT_malus_bool = wuchtans + finteans + malusval <= AT - 1

#            if previous_hit_bool == "D":
#                if AT_malus_bool == True and AT_norm_bool == True:
#                    if current_hit_bool == "T":
#                        hit_prob_list.append(prob_malus(AT, PA, wuchtans, finteans, malusval))
#                        damage_list.append(dmg + wuchtans)
#                    else:
#                        hit_prob_list.append(1 - prob_malus(AT, PA, wuchtans, finteans, malusval))
#
#            elif current_hit_bool == "T":
#                if AT_norm_bool == True:
#                    if current_hit_bool == "T":
#                        hit_prob_list.append(prob_norm(AT, PA, wuchtans, finteans))
#                        damage_list.append(dmg + wuchtans)
#                    else:
#                        hit_prob_list.append(1 - prob(AT, PA, wuchtans, finteans))



            if previous_hit_bool == "T":
                if AT_norm_bool == True:
                    if current_hit_bool == "T":
                        hit_prob_list.append(prob_normal(AT, PA, wuchtans, finteans))
                        damage_list.append(dmg + wuchtans)
                    else:
                        hit_prob_list.append(1 - prob_normal(AT, PA, wuchtans, finteans))

            elif previous_hit_bool == "D":
                if current_hit_bool == "T":
                    hit_prob_list.append(
                        prob_malus(AT, PA, wuchtans, finteans, malusval))
                    damage_list.append(dmg + wuchtans)
                else:
                    hit_prob_list.append(
                        1 - prob_malus(AT, PA, wuchtans, finteans, malusval))

        einzel_erwartungswert_list.append(np.prod(hit_prob_list) * np.sum(damage_list))

    return einzel_erwartungswert_list


def Angriffsketten_Ansagenoptimierer(AT, PA, dmg, num_attacks):
    finte_max = PA - 1
    Wucht_max = AT - 1
    dimension_finte = [finte_max + 1 for i in range(num_attacks)]
    dimension_wucht = [Wucht_max for i in range(num_attacks)]
    erwartungswert_array_dimension = dimension_finte + dimension_wucht
    erwartungswert_array = np.zeros(erwartungswert_array_dimension)

    for idx, val in np.ndenumerate(erwartungswert_array):
        erwartungswert_ergebnis_list = Erwartungswert(AT, PA, dmg, idx[:num_attacks], idx[num_attacks:],
                                                      num_attacks)
        erwartungswert_array[idx] = np.sum(erwartungswert_ergebnis_list)

    erwartungswert_endliste = []
    finte_endliste = []
    wucht_endliste = []

    for idx, val in np.ndenumerate(erwartungswert_array):
        erwartungswert_endliste.append(val)
        finte_endliste.append(idx[:num_attacks])
        wucht_endliste.append(idx[num_attacks:])

    erwartungswert_liste_sortiert, sorted_indice = zip(
        *sorted(zip(erwartungswert_endliste, range(len(erwartungswert_endliste)))))

    for i in sorted_indice:
        erw_val = round(erwartungswert_endliste[i], 4)
        finte_val = finte_endliste[i]
        wucht_val = wucht_endliste[i]
        print("Erwartungswert: " + str(erw_val) + ", Finteansage: " + str(finte_val) + ", Wuchtansage: " + str(
            wucht_val))



Angriffsketten_Ansagenoptimierer(10, 10, 5, 3)
