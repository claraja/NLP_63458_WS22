Erstellung der Dokumentation mit sphinx

https://sphinx-rtd-tutorial.readthedocs.io/en/latest/build-the-docs.html
https://shunsvineyard.info/2019/09/19/use-sphinx-for-python-documentation/

Note: when we add a new module, class, API, or any code change that affects the documents, we need to repeat Step 3 and Step 4 to update the documents:
Step 3: aus dem Verzeichnis: \MedExtractor\docs> sphinx-apidoc -f -o source/ ../medextractor/

vorherige html- und pdf-Doku löschen: make clean html

neue html-doku erstellen: make html

neue pdf-Doku erstellen: make latexpdf (erzeugt pdf-doku in: MedExtractor\docs\build\latex)



create a new readme.rst: pandoc --from=markdown --to=rst --output=README.rst README.md

