"""passDouche.py: Determine whether a card is ready to be sent."""

__author__ = "Arnaud Petit"

import os
import time
import pyfiglet

from core import test, initialisation, enregistrer, done


def boucle():

    while (True):
        os.system('color 0B')
        os.system('cls')
        print("=" * 80)
        print("\n\n\t\t\t")
        ascii_banner = pyfiglet.figlet_format("PRET : DOUCHER")
        print(ascii_banner)
        print("\n\n\n" + "=" * 80)

        inputUser = ""
        while inputUser == "":
            inputUser = str(input())

        resultat = test(inputUser)

        if resultat == "pass":

            os.system('color 2E')
            ascii_banner = pyfiglet.figlet_format("PASS")
            print(ascii_banner)

        elif resultat == "lackOfTest":

            os.system('color 5E')
            ascii_banner = pyfiglet.figlet_format("REPASSER TEST")
            print(ascii_banner)

        elif resultat == "abort":

            os.system('color E0')
            ascii_banner = pyfiglet.figlet_format("TEST ABORTED")
            print(ascii_banner)

        elif resultat == "unexpected":

            os.system('color F0')
            ascii_banner = pyfiglet.figlet_format("UNEXPECTED")
            print(ascii_banner)

        else:

            os.system('color CE')
            ascii_banner = pyfiglet.figlet_format("FAIL")
            print(ascii_banner)
            print(resultat)

        enregistrer(inputUser, resultat)
        time.sleep(0.45)


if __name__ == "__main__":
    initialisation()
    boucle()
    done()
