CeviDB Tool
===========

Das CeviDB Tool erlaubt es Listen mit den Mitgliedern
von CeviDB-Gruppen zu führen, in denen zusätzliche
Informationen zu den einzelnen Mitgliedern geführt werden.
Das Tool aktualisiert die Adress-Daten der Mitglieder
ohne die zusätzlichen Informationen zu verändern.


Installation
------------

* Install Python, pip and pipenv for your OS (you most likely want to install python into `PATH`)
* download/clone this repository
* run `pipenv install -r requirements.txt` (you might need to adjust the version of `wxpython` if pipenv fails to build it)
* run `pipenv run python cevidbtool.py` (or use the corresponding helper-script for your os)

Nutzung
-------

* Konfigurationsdatei config.ini erstellen
  (vgl. examples/config.ini; groupid muss angepasst werden)
* Tool starten (cevidbtool.py)
* E-Mail-Adresse und Passwort eintragen
* xlsx-Datei auswählen
  (vgl. examples/spender.xlsx, zu examples/config.ini)
* aktualisieren klicken und auf Bestätigung warten.


