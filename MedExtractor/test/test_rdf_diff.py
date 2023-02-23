from rdflib import Graph
from rdflib.compare import to_isomorphic, graph_diff
from rdflib import Namespace, Graph, URIRef, Literal
import pandas as pd


def dump_nt_sorted(g):
    print()
    for l in sorted(g.serialize(format='nt').splitlines())[:]:
        if l: print(l)

def add_symptom(symptom_str: str, graph: Graph):
    symptom_uri = URIRef(namespace_string + symptom_str.replace(' ', '_'))
    graph.add((depression, hasSymptom, symptom_uri))



if __name__ == "__main__":

    namespace_string = "http://fapranlp.de/"
    namespace = Namespace(namespace_string)
    output_path = "../resources/manual_text_to_analyze.xml"
    prefix = "fapra"
    # Create a Graph
    g3 = Graph()
    # namespace_manager3 = g3.namespace_manager
    # namespace_manager3.bind(prefix, namespace)
    g4 = Graph()
    # namespace_manager4 = g4.namespace_manager
    # namespace_manager4.bind(prefix, namespace)
    #
    depression = URIRef(namespace_string + "depression")
    hasSymptom = URIRef(namespace_string + "hasSymptom")
    #
    # symptoms3 = ["continuous low mood", "sadness", "feeling hopeless and helpless", ]
    # symptoms4 = ["sadness", "feeling hopeless and helpless", "low self-esteem",
    #              "feeling tearful"]
    #
    # for symptom in symptoms3:
    #     add_symptom(symptom, g3)
    #
    #
    # for symptom in symptoms4:
    #     add_symptom(symptom, g4)

    g3.parse("../resources/diff_test_rdf.xml")
    g4.parse("../resources/manual_text_to_analyze.xml")

    iso1 = to_isomorphic(g3)
    iso2 = to_isomorphic(g4)

    print(iso1 == iso2)

    in_both, in_first, in_second = graph_diff(iso1, iso2)


    print(in_both)
    print(in_first)
    print(in_second)

    dump_nt_sorted(in_both)

    dump_nt_sorted(in_first)
    dump_nt_sorted(in_second)

    print(f"Graph in_both has {len(in_both)} statements.")
    print(f"Graph in_first has {len(in_first)} statements.")
    print(f"Graph in_second has {len(in_second)} statements.")
    df = pd.DataFrame()
    print(df.size)