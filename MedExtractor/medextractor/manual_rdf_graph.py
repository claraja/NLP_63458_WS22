from rdflib import Namespace, Graph, URIRef, Literal


def add_symptom(symptom_str: str):
    symptom_uri = URIRef(namespace_string + symptom_str.replace(' ', '_'))
    g.add((depression, hasSymptom, symptom_uri))


namespace_string = "http://fapranlp.de/"
namespace = Namespace(namespace_string)
output_path = "../resources/manual_text_to_analyze.xml"
prefix = "fapra"
# Create a Graph
g = Graph()
namespace_manager = g.namespace_manager
namespace_manager.bind(prefix, namespace)

depression = URIRef(namespace_string + "depression")
hasSymptom = URIRef(namespace_string + "hasSymptom")

symptoms = ["continuous low mood", "sadness", "feeling hopeless and helpless", "low self-esteem", "feeling tearful",
            "feeling guilt-ridden", "feeling irritable and intolerant of others",
            "having no motivation or interest in things", "finding it difficult to make decisions",
            "not getting any enjoyment out of life", "feeling anxious or worried",
            "suicidal thoughts", "thoughts of harming yourself",
            "moving or speaking more slowly than usual", "changes in appetite or weight", "constipation",
            "unexplained aches and pains", "lack of energy", "low sex drive (loss of libido)",
            "changes to your menstrual cycle", "disturbed sleep", "finding it difficult to fall asleep at night",
            "waking up very early in the morning",
            "avoiding contact with friends", "taking part in fewer social activities",
            "neglecting your hobbies and interests", "having difficulties in your home, work or family life"]

for symptom in symptoms:
    add_symptom(symptom)

g.serialize(format='pretty-xml', destination=output_path)

