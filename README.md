CeviDB Tool
===========

Das CeviDB Tool erlaubt es Listen mit den Mitgliedern
von CeviDB-Gruppen zu führen, in denen zusätzliche
Informationen zu den einzelnen Mitgliedern geführt werden.
Das Tool aktualisiert die Adress-Daten der Mitglieder
ohne die zusätzlichen Informationen zu verändern.


Installation
------------

* Abhängigkeiten
  Damit das CeviDB Tool funktioniert müssen die folgenden
  Software-Pakete installiert sein:

    * Python (2.7.x):     https://www.python.org/
    * wxPython (3.0.1.1): http://www.wxpython.org/
    * openpyxl (2.1.4):   https://pypi.python.org/pypi/openpyxl
    * requests (2.3.0):   https://pypi.python.org/pypi/requests

  Die Versionsnummern bezeichnen die für die Entwicklung verwendeten
  Versionen.


Nutzung
-------

* Konfigurationsdatei config.ini erstellen
  (vgl. examples/config.ini; groupid muss angepasst werden)
* Tool starten (cevidbtool.py)
* E-Mail-Adresse und Passwort eintragen
* xlsx-Datei auswählen
  (vgl. examples/spender.xlsx, zu examples/config.ini)
* aktualisieren klicken und auf Bestätigung warten.


