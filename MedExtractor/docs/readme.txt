Erstellung der Dokumentation mit sphinx

https://shunsvineyard.info/2019/09/19/use-sphinx-for-python-documentation/

Note: when we add a new module, class, API, or any code change that affects the documents, we need to repeat Step 3 and Step 4 to update the documents:
Step 3: sphinx-apidoc -f -o source/ ../medextractor/

make html

make clean html


create a new readme.rst: pandoc --from=markdown --to=rst --output=README.rst README.md

make latexpdf
erzeugt pdf-doku in: MedExtractor\docs\build\latex
