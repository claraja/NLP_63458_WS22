"""
Program for "manual" creation of an RDF-Graph: 
Disease and corresponding symptoms are given, an RDF-Graph is built and saved as xml-file.
"""

from rdflib import Namespace, Graph, URIRef, Literal


def add_symptom(symptom_str: str):
    symptom_uri = URIRef(namespace_string + symptom_str.replace(' ', '_'))
    g.add((depression, hasSymptom, symptom_uri))

if __name__ == "__main__":

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

    symptoms = {"depression": ["continuous low mood", "sadness", "feeling hopeless and helpless", "low self-esteem", "feeling tearful",
                            "feeling guilt-ridden", "feeling irritable and intolerant of others",
                            "having no motivation or interest in things", "finding it difficult to make decisions",
                            "not getting any enjoyment out of life", "feeling anxious or worried",
                            "suicidal thoughts", "thoughts of harming yourself",
                            "moving or speaking more slowly than usual", "changes in appetite or weight", "constipation",
                            "unexplained aches and pains", "lack of energy", "low sex drive (loss of libido)",
                            "changes to your menstrual cycle", "disturbed sleep", "finding it difficult to fall asleep at night",
                            "waking up very early in the morning",
                            "avoiding contact with friends", "taking part in fewer social activities",
                            "neglecting your hobbies and interests", "having difficulties in your home, work or family life"],
                "Anxiety Disorders":["worry", "temporary worry","fear", "anxiety", "interfere with daily activities",
                                     "persistent feeling of anxiety or dread", "Feeling restless", "feeling wound-up",
                                    "feeling on-edge", "being easily fatigued", "having difficulty concentrating",
                                     "being irritable", "headaches", "muscle aches", "stomachaches", "unexplained pains",
                                     "difficulty controlling feelings of worry", "sleep problems", "difficulty falling",
                                    "difficulty staying asleep", "sudden periods of intense fear", "discomfort",
                                     "sense of losing control", "pounding heart", "racing heart", "sweating", "trembling",
                                    "tingling", "chest pain", "feelings of impending doom", "feelings of being out of control",
                                     "avoiding places", "avoiding situations", "avoiding behaviors",
                                     "fear of being watched and judged by others", "blushing", "sweating", "trembling",
                                     "pounding heart", "racing heart", "stomachaches", "rigid body posture",
                                    "speaking with an overly soft voice", "difficulty making eye contact",
                                    "difficulty being around people they don’t know", "feelings of self-consciousness",
                                    "fear that people will judge them negatively"],
                "Bulimia":["eating a large amount of food over a very short time (binge eating)",
                           "ridding your body of the extra food (purging)" , "making yourself vomit",
                           "taking laxatives", "exercising excessively", "fear of putting on weight",
                           "being very critical about your weight and body shape", "mood changes", "feeling very tense",
                           "feeling very anxious", "thinking about food a lot", "feeling guilty", "feeling ashamed",
                           "behaving secretively", "avoiding social activities that involve food",
                           "feeling like you have no control over your eating", "feeling tired",
                           "a sore throat from being sick", "bloating", "tummy pain", "puffy face", "self-harming",
                           "eating a lot of food, very fast", "going to the bathroom a lot after eating",
                           "excessively or obsessively exercising"],
                "Claustrophobia": ["irrational fear of confined spaces", "avoid confined spaces",
                                   "mild anxiety when in a confined space", "severe anxiety","panic attack",
                                   "feeling of losing control", "fear of losing control",
                                   "thinking about certain situations", "felt anxious about being in a confined space",
                                  "felt anxious about being in a crowded place", "panic attacks", "frightening", "distressing",
                                   "sweating", "trembling", "hot flushes or chills", "shortness of breath", "difficulty breathing",
                                   "a choking sensation", "a rapid heartbeat(tachycardia)", "chest pain",
                                   "feeling of tightness in the chest", "a sensation of butterflies in the stomach", "feeling sick",
                                   "headaches", "dizziness", "feeling faint", "numbness", "pins and needles", "a dry mouth",
                                   "a need to go to the toilet", "ringing in your ears", "feeling confused", "feeling disorientated",
                                   "fear of losing control", "fear of fainting", "feelings of dread", "fear of dying"]


}

    for symptom in symptoms:
        add_symptom("symptom:" + symptom)

    g.serialize(format='pretty-xml', destination=output_path)

