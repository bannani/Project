# coding: utf-8
from argparse import ArgumentParser, RawTextHelpFormatter

def get_args():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "--mode",
        help="""Mode d'utilisation du programme : 'train_test' ou 'use' (OBLIGATOIRE)
    - train_test: Entraîne le modèle sur les données d'entraînement et teste le modèle sur les données de test
    - use: Utilise le modèle pour classifier de nouveaux chiffres""",
        required=True
    )
    parser.add_argument(
        "--model",
        help="Nom du modèle : 'NN1', 'NN2', 'NN3', 'NN4', 'NN5', 'NN6', 'NN7', 'NN8', 'NN9' (défaut: NN7)",
        default="NN7"
    )
    return parser.parse_args()
