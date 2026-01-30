import storage

def run():
    storage.init_storage()

    # Sections
    sections = storage.get_sections()
    if not sections:
        new_sections = [
            "Arts Martiaux", "Athlétisme", "Badminton", "Basketball", "Boxe",
            "Escrime", "Football", "Grappling", "Gymnastique", "Handball",
            "Marche Nordique", "Multisports", "Natation", "Omnisports",
            "Plongée Apnée NAP", "Taekwondo", "Tennis", "Yoga"
        ]
        storage.save_sections(new_sections)

    # Form 1: Budget
    if not storage.get_template(1):
        struct = {
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
                        {"id": "h_ben_occ", "label": "Nb d'heures annuelles (Occasionnels)", "type": "number"},
                    ]
                },
                {
                    "title": "2 - Recettes",
                    "fields": [
                        {"id": "cot_nb", "label": "Nombre d'adhérents cotisants", "type": "number"},
                        {"id": "cot_prix", "label": "Prix moyen de cotisation", "type": "number"},
                        {"id": "cot_club", "label": "Cotisation Club (Prélèvement 20€)", "type": "number", "multiplier": 20, "source": "cot_nb"},
                        {"id": "sub_hors_mairie", "label": "Subvention hors mairie", "type": "number"},
                        {"id": "sponsors", "label": "Sponsors / Mécène", "type": "number"},
                        {"id": "recettes_evt", "label": "Recettes événementiel", "type": "number"},
                        {"id": "part_equip", "label": "Participation équipement", "type": "number"},
                        {"id": "part_depl", "label": "Participation déplacements", "type": "number"},
                        {"id": "part_stages", "label": "Participation stages", "type": "number"},
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
                    ]
                },
                {
                    "title": "4 - Solde et Demande",
                    "fields": [
                        {"id": "sub_demandee", "label": "Subvention demandée", "type": "number"},
                        {"id": "justification", "label": "Justification de la demande", "type": "textarea"},
                    ]
                }
            ]
        }
        storage.save_template_version(1, struct)

    # Form 2: Bureau
    if not storage.get_template(2):
        struct = {
            "type": "fixed_table",
            "cols": ["Président", "Trésorier", "Secrétaire"],
            "rows": [
                {"id": "nom", "label": "Nom"},
                {"id": "prenom", "label": "Prénom"},
                {"id": "email", "label": "Adresse mail"},
                {"id": "tel", "label": "Tel Portable"}
            ]
        }
        storage.save_template_version(2, struct)

    # Form 3: Formation
    if not storage.get_template(3):
        struct = {
            "type": "dynamic_table",
            "cols": [
                {"id": "nom", "label": "Nom"},
                {"id": "prenom", "label": "Prénom"},
                {"id": "bpjeps", "label": "BPJEPS"},
                {"id": "be", "label": "BE"},
                {"id": "federal", "label": "FEDERAL"},
                {"id": "autre", "label": "AUTRE"},
                {"id": "appellation", "label": "Appellation"},
                {"id": "v2025", "label": "2025"},
                {"id": "v2026", "label": "2026"},
                {"id": "v2027", "label": "2027"},
                {"id": "organisme", "label": "Organisme"}
            ]
        }
        storage.save_template_version(3, struct)

    # Form 4: Salariés
    if not storage.get_template(4):
        struct = {
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
        storage.save_template_version(4, struct)

    print("Initialisation des fichiers JSON terminée.")

if __name__ == '__main__':
    run()
