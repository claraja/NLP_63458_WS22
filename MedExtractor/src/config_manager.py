import json
import os


class ConfigManager:
    def __init__(self):
        try:
            with open("config.json", "r") as jsonfopen:
                json_read = json.load(jsonfopen)
        except FileNotFoundError:
            jsoncontent = {
                "RDF_filename": "path/name.xml",
                "EntityLinkerExport_filename": "path/name.xml",
                "KnowledgeBase_filename": "path/name.kb",
                "Sample_text_folder": "path",
                "Overwrite existing knowledgebase file": "False",
                "Diseases_filename": "path/name.txt",
                "Symptoms_filename": "path/name.txt",
            }
            with open("config.json", "w") as jsonfopen:
                json.dump(jsoncontent, jsonfopen, indent=4)
            print("No file config.json in folder. New file was created as " + os.path.abspath(
                jsonfopen.name) + ". Please update this json-file before starting Medextractor again.")
            quit()

        try:
            self.relations_filename = json_read["RDF_filename"]
        except KeyError:
            print("No RDF file name in config.json.")
            quit()

        try:
            self.entity_linker_export_filename = json_read["EntityLinkerExport_filename"]
        except KeyError:
            print("No entity linker export file name in config.json.")
            quit()

        try:
            self.knowledgebase_filename = json_read["KnowledgeBase_filename"]
        except KeyError:
            print("No knowledgebase file name in config.json.")
            quit()

        try:
            self.text_folder_name = json_read["Sample_text_folder"]
        except KeyError:
            print("No text folder file name in config.json.")
            quit()

        try:
            self.diseases_filename = json_read["Diseases_filename"]
        except KeyError:
            print("No diseases file name in config.json.")
            quit()

        try:
            self.symptoms_filename = json_read["Symptoms_filename"]
        except KeyError:
            print("No symptoms file name in config.json.")
            quit()

        try:
            self.overwrite = True if json_read["Overwrite existing knowledgebase file"] == "True" else False
        except KeyError:
            print("No overwrite specification in config.json.")
            quit()