import os
import json
import pandas as pd
import storage

def initialize_from_scratch():
    storage.init_storage()

    # 1. Sections
    sections = [
        "Arts Martiaux", "Athlétisme", "Badminton", "Basketball", "Boxe",
        "Escrime", "Football", "Grappling", "Gymnastique", "Handball",
        "Marche Nordique", "Multisports", "Natation", "Omnisports",
        "Plongée Apnée NAP", "Taekwondo", "Tennis", "Yoga"
    ]
    for s in sections:
        storage.add_section(s)

    # 2. Theme 1 (Budget) - V5
    budget_v5 = {
        "type": "budget",
        "groups": [
            {
                "title": "1 - Informations Générales",
                "fields": [
                    {"id": "fed", "label": "Fédération", "type": "text"},
                    {"id": "nb_lic", "label": "Nb adhérents licencié/assuré", "type": "number"},
                    {"id": "nb_non_lic", "label": "Nb adhérents non licencié", "type": "number"},
                    {"id": "nb_fem", "label": "Nb Féminines 2024-2025", "type": "number"},
                    {"id": "nb_fem_18", "label": "dont - de 18 ans", "type": "number"},
                    {"id": "nb_masc", "label": "Nb Masculins 2024-2025", "type": "number"},
                    {"id": "nb_masc_18", "label": "dont - de 18 ans", "type": "number"},
                    {"id": "nb_entraineurs", "label": "Nb Entraineurs", "type": "number"},
                    {"id": "nb_ben_perm", "label": "Nb de Bénévoles Permanents", "type": "number"},
                    {"id": "h_ben_perm", "label": "Nb d'heures annuelles (Permanents)", "type": "number"},
                    {"id": "nb_ben_occ", "label": "Nb de Bénévoles Occasionnels", "type": "number"},
                    {"id": "h_ben_occ", "label": "Nb d'heures annuelles (Occasionnels)", "type": "number"}
                ]
            },
            {
                "title": "2 - Recettes - A - Cotisations",
                "fields": [
                    {"id": "cot_nb", "label": "Nombre d'adhérents cotisants", "type": "number"},
                    {"id": "cot_prix", "label": "Prix moyen de cotisation", "type": "number"},
                    {"id": "cot_brut", "label": "Recettes cotisations", "type": "number", "formula": "cot_nb * cot_prix"}
                ]
            },
            {
                "title": "2 - Recettes - B - Cotisation Club",
                "fields": [
                    {"id": "cot_club", "label": "Prélèvement 20€", "type": "number", "formula": "cot_nb * 20"},
                    {"id": "cot_net", "label": "Recettes totales cotisations", "type": "number", "formula": "cot_brut - cot_club"}
                ]
            },
            {
                "title": "2 - Recettes - C - Autres produits",
                "fields": [
                    {"id": "subventions", "label": "Subventions", "type": "number"},
                    {"id": "partenariats", "label": "Partenariats", "type": "number"},
                    {"id": "manifestations", "label": "Manifestations", "type": "number"},
                    {"id": "autres_produits", "label": "Autres", "type": "number"},
                    {"id": "total_autres", "label": "Recettes autres produits", "type": "number", "formula": "subventions + partenariats + manifestations + autres_produits"},
                    {"id": "total_recettes", "label": "Recettes totales", "type": "number", "formula": "cot_net + total_autres"}
                ]
            },
            {
                "title": "3 - Dépenses",
                "fields": [
                    {"id": "dep_materiel", "label": "Matériel et équipement", "type": "number"},
                    {"id": "dep_evt", "label": "Evénementiel", "type": "number"},
                    {"id": "dep_stages", "label": "Stages", "type": "number"},
                    {"id": "dep_formation", "label": "Formation", "type": "number"},
                    {"id": "dep_depl", "label": "Déplacements", "type": "number"},
                    {"id": "dep_gestion", "label": "Frais de gestion", "type": "number"},
                    {"id": "dep_affiliation", "label": "Affiliation", "type": "number"},
                    {"id": "dep_arbitrage", "label": "Arbitrage et Juge", "type": "number"},
                    {"id": "dep_licences", "label": "Licences", "type": "number"},
                    {"id": "dep_salaires", "label": "Salaires (Charges incluses)", "type": "number"},
                    {"id": "dep_defraiements", "label": "Défraiements", "type": "number"},
                    {"id": "dep_total", "label": "TOTAL DEPENSES", "type": "number", "formula": "dep_materiel + dep_evt + dep_stages + dep_formation + dep_depl + dep_gestion + dep_affiliation + dep_arbitrage + dep_licences + dep_salaires + dep_defraiements"}
                ]
            },
            {
                "title": "4 - Solde et Demande",
                "fields": [
                    {"id": "sub_demandee", "label": "Subvention demandée", "type": "number"},
                    {"id": "resultat_prev", "label": "Résultat prévisionnel", "type": "number", "formula": "total_recettes - dep_total"},
                    {"id": "justification", "label": "Justification de la demande", "type": "textarea"}
                ]
            }
        ]
    }
    storage.save_template_version(1, budget_v5, version=5)

    # 3. Theme 2 (Bureau)
    bureau_v1 = {
        "type": "fixed_table",
        "cols": ["Président", "Trésorier", "Secrétaire"],
        "rows": [
            {"id": "nom", "label": "Nom"},
            {"id": "prenom", "label": "Prénom"},
            {"id": "email", "label": "Adresse mail"},
            {"id": "tel", "label": "Tel Portable"}
        ]
    }
    storage.save_template_version(2, bureau_v1, version=1)

    # 4. Theme 3 (Formation)
    formation_v1 = {
        "type": "dynamic_table",
        "cols": [
            {"id": "nom", "label": "Nom"}, {"id": "prenom", "label": "Prénom"},
            {"id": "bpjeps", "label": "BPJEPS"}, {"id": "be", "label": "BE"},
            {"id": "federal", "label": "FEDERAL"}, {"id": "autre", "label": "AUTRE"},
            {"id": "appellation", "label": "Appellation"}, {"id": "v2025", "label": "2025"},
            {"id": "v2026", "label": "2026"}, {"id": "v2027", "label": "2027"},
            {"id": "organisme", "label": "Organisme"}
        ]
    }
    storage.save_template_version(3, formation_v1, version=1)

    # 5. Theme 4 (Salariés)
    salaries_v1 = {
        "type": "dynamic_table",
        "cols": [
            {"id": "nom_prenom", "label": "Noms et Prénom"},
            {"id": "type_contrat", "label": "Type de contrat"},
            {"id": "taux_horaire", "label": "Taux horaire Net"},
            {"id": "heures_hebdo", "label": "Heures hebdomadaires"},
            {"id": "nb_semaines", "label": "Nombre de semaines"},
            {"id": "mutuelle", "label": "Mutuelle club"}
        ]
    }
    storage.save_template_version(4, salaries_v1, version=1)

if __name__ == "__main__":
    initialize_from_scratch()
    print("Base de données initialisée avec succès (Structure Budget V5).")
