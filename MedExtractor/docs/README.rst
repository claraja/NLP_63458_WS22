Erstellung der Dokumentation mit sphinx
=======================================

Links:
------

-  https://sphinx-rtd-tutorial.readthedocs.io/en/latest/build-the-docs.html
-  https://shunsvineyard.info/2019/09/19/use-sphinx-for-python-documentation/

..

   **NOTE:** Nach dem Hinzufügen eines neuen Moduls, einer neuen Klasse
   oder API, oder einer anderen Änderung des Codes, müssen Schritt 3 und
   4 wiederholt werden um die Dateien zu aktualisieren.

-  Schritt 3: aus dem Verzeichnis:
   :raw-latex:`\MedExtractor`:raw-latex:`\docs`> sphinx-apidoc -f -o
   source/ ../medextractor/
-  vorherige html- und pdf-Doku löschen: make clean html
-  neue html-doku erstellen: make html
-  neue pdf-Doku erstellen: make latexpdf (erzeugt pdf-doku in:
   MedExtractor:raw-latex:`\docs`:raw-latex:`\build`:raw-latex:`\latex`)
-  neue readme.rst erstellen: pandoc –from=markdown –to=rst
   –output=README.rst README.md
