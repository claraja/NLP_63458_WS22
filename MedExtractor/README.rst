Fachpraktikum WS 22/23 - Natural Language Processing (NLP) mit spaCy
====================================================================

Medextractor - Konsolenapplikation
==================================

Die Medextractor-Konsolenapplikation analysiert Texte und sucht darin
nach Krankheiten und deren Symptomen und erstellt eine
Wissensrepräsentation, die die gefundenen Krankheiten und Symptome
miteinander in Beziehung setzt. Die Wissensrepräsentation wird im RDF
(Resource Discription Framework)-Format gespeichert. Zusätzlich erstellt
der Medextractor eine xml-Datei mit Daten für den Entity Linker von
spaCy sowie eine Datei name.kb, in dem die erstellte Wissensbasis in
Binärcode abgespeichert wird.

Ordnerstruktur
==============

-  **docs**: mit Sphinx erstellte Dokumentation des
   MedExtractor-Programms, mit Öffnen der html-Dateien in docs/build
   kommt man zu einer ansprechenden Dokumentation des Programms
-  **medextractor**: enthält die Programme, die für die Erstellung der
   Wissensbasis zuständig sind

   -  **preprocessor**: Programm, das einen gegebenen Text
      vorverarbeitet, sodass es in weiteren Schritten besser verarbeitet
      werden kann
   -  **knowledge**: verarbeitet vorverarbeiteten Text, extrahiert
      Krankheiten und dazugehörige Symptome und speichert sie in einer
      Knowledgebase
   -  **rdf**: Serialisiert die erstellte Knowledgebase und speichert
      sie als xml-Datei im RDF-Format

-  **resources**: alle Ressourcen, die zum Ausführen des Programms
   benötigt werde, sowie Ausgabedateien

   -  **to_analyze**: Texte, die vom Programm analysiert und ausgewertet
      werden können
   -  **training_data**: Vokabular-Dateien (siehe Abschnitt unten)

-  **test**: Testprogramme

Konfigurationsdatei config.json
===============================

Das Python-Modul, mit dem die Konsolenapplikation gestartet wird, ist
die Datei: medextractor.py. Im selben Order von medextractor.py muss
sich die Konfigurationsdatei config.json befinden.

Sollte es noch keine config.json Datei geben, wird beim Aufruf von
medextractor.py eine Beispiel-Datei erzeugt, die anschließend vom Nutzer
angepasst werden muss.

Die Konfigurationsdatei enthält folgende Informationen:

1. Pfad und Name der xml-Datei für den Export im RDF-Format
2. Pfad und Name der xml-Datei für den Export für den Entity Linker
3. Pfad und Name der KnowledgeBase Datei
4. Pfad zu dem Order, der die zu analysierenden Texte enthält
5. Spezifikation, ob die Knowledgebase Datei überschrieben werden soll
   (True oder False)
6. Pfad und Name der .txt-Datei, die das Krankheiten-Vokabular enthält
7. Pfad und Name der .txt-Datei, die das Symptome-Vokabular enthält

Die Pfade müssen relativ zu dem Order angegeben werden, in dem sich
medextractor.py befindet. Alternativ können auch absolute Pfade angeben
werden.

Es werden alle Textdateien (*.txt) analysiert, die sich in dem in der
config.json-Datei angegebenen Ordner befinden. Die von Medextractor
erzeugten xml- und Knowledgebase- Dateien enthalten ein über alle
analysierten Texte akkumuliertes Ergebnis.

Wird festgelegt, dass die Knowledgebase-Datei nicht überschrieben werden
soll, werden alle neu gefundenen Krankheit-Symptom-Beziehungen zu der
vorhandenen Knowledgebase-Datei hinzugefügt.

Vokabular-Dateien
=================

Die Vokabulardateien sind einfache Dateien im csv-Format und enthalten
Einträge der folgenden Art:

C0010051 coronary aneurysm DISEASE

Der Eintrag C0010051 ist der CUI (Concept Unique Identifier) aus der
MetaMapLite-Datenbank. Der CUI ist als Referenz enthalten, wird aber
nicht weiter vom Medextractor verwendet.

Aufruf des Programms
====================

Voraussetzungen
---------------

-  eine Python Version 3.6-3.8 (empfohlen und getestet: 3.8) muss
   installiert sein (SpaCy ist noch nicht kompatibel mit Python >3.8)
-  Packages, die in requirements.txt aufgelistet sind, sind installiert
   (Installation aller Packages möglich mit dem Befehl
   ``pip install -r requirements.txt``)

Aufruf
------

Das Programm wird gestartet, indem in die Windowseingabeaufforderung der
Befehl

``python medextractor.py``

eingegeben wird.

Zu beachten ist, dass in der System-Path-Umgebungsvariable der Pfad zur
(ggf. virtuellen) Umgebung des Python-Interpreters enthalten ist, in der
spaCy installiert wurde. Ggf. sollte hierzu activate.bat im Verzeichnis
der virtuellen Umgebung der Python-Installation aufgerufen werden.

Da die Vokabulardateien umfangreich sind, kann allein das Trainieren des
Entity-Rulers (je nach Rechner) eine Minute übersteigen.

Nach Beendigung des Programms befinden sich die xml-Dateien mit der
RDF-Repräsentation sowie die xml-Datei für den Entity Linker in dem in
config.json angegebenen Ordner.

Entity-Linker
=============

Das Jupyter-Notebook entity_linker_demo.ipynb (zu finden im Ordner
NLP_63458_WS22/notebooks/entity_linker_demo.ipynb) demonstriert, wie die
Daten aus der xml-Export-Datei gelesen und für das Training von Entity
Ruler und Entity Linker verwendet werden. Findet der Entity Ruler in
einem Text Symptome, dann ordnet der Entity Linker diesen Symptome
dazugehörige Krankheiten zu.
