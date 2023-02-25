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
                                       "fear of losing control", "fear of fainting", "feelings of dread", "fear of dying"],
                    "Dementia":["loss of cognitive functioning", "cannot control their emotions", "personalities may change",
                                "depend completely on others for basic activities of living", "memory loss", "poor judgment",
                                "confusion", "difficulty speaking, understanding and expressing thoughts, or reading and writing",
                                "wandering", "getting lost in a familiar neighborhood", "trouble handling money responsibly and paying bills",
                                "repeating questions", "using unusual words to refer to familiar objects",
                                "taking longer to complete normal daily tasks", "losing interest in normal daily activities or events",
                                "hallucinating", "experiencing delusions or paranoia", "acting impulsively",
                                "not caring about other people’s feelings", "losing balance", "problems with movement"],
                    "Eating disorders": ["eating too much or too little", "worrying about your weight or body shape",
                                         "anorexia nervosa", "trying to control your weight", "not eating enough food",
                                         "exercising too much", "bulimia", "losing control over how much you eat",
                                         "taking drastic action to not put on weight", "binge eating disorder(BED)",
                                         "eating large portions of food until you feel uncomfortably full",
                                         "avoids certain foods", "limits how much they eat",
                                         "spending a lot of time worrying about your weight and body shape",
                                         "avoiding socialising when you think food will be involved", "eating very little food",
                                         "making yourself sick", "taking laxatives after you eat", "exercising too much",
                                         "having very strict habits or routines around food", "changes in your mood",
                                         "being withdrawn, anxious or depressed", "feeling cold, tired or dizzy",
                                         "pains, tingling or numbness in your arms and legs(poor circulation)",
                                         "feeling your heart racing", "fainting", "feeling faint", "problems with your digestion",
                                         "bloating", "constipation", "diarrhoea",
                                         "you weight being very high or very low for someone of your age and height",
                                         "not getting your period", "delayed signs of puberty", "dramatic weight loss",
                                         "lying about how much they've eaten, when they' ve eaten, or their weight",
                                         "eating a lot of food very fast", "going to the bathroom a lot after eating",
                                         "exercising a lot", "avoiding eating with others", "cutting food into small pieces or eating very slowly",
                                         "wearing loose or baggy clothes to hide their weight loss"],
                    "Panic disorder": ["regularly have sudden attacks of panic or fear", "anxiety", "panic", "panic attacks",
                                       "a racing heartbeat", "feeling faint", "sweating", "nausea", "chest pain",
                                       "shortness of breath", "trembling", "hot flushes", "chills", "shaky limbs",
                                       "a choking sensation", "dizziness", "numbness or pins and needles", "dry mouth",
                                       "a need to go to the toilet", "ringing in your ears", "a feeling of dread or a fear of dying",
                                       "a churning stomach", "a tingling in your fingers", "feeling like you're not connected to your body"],
                    "Psychosis":["hallucinations", "seeing colours, shapes or people","hearing voices or other sounds",
                                 "feeling touched when there is nobody there", "an odour that other people cannot smell",
                                 "a taste when there is nothing in the mouth", "delusions", "confused and disturbed thoughts",
                                 "disturbed, confused, and disrupted patterns of thought", "rapid and constant speech",
                                 "disturbed speech", "switch from one topic to another mid-sentence",
                                 "a sudden loss in their train of thought", "an abrupt pause in conversation or activity",
                                 "high mood(mania)", "feeling elated", "talking and thinking too much or too quickly",
                                 "low mood", "feeling sad", "lack of energy", "loss of appetite", "trouble sleeping"],
                    "Social anxiety": ["fear of social situations",
                                       "worry about everyday activities, such as meeting strangers, starting conversations, speaking on the phone, working or shopping",
                                       "avoid or worry a lot about social activities, such as group conversations, eating with company and parties",
                                       "always worry about doing something you think is embarrassing, such as blushing, sweating or appearing incompetent",
                                       "find it difficult to do things when others are watching", "feel like you're being watched and judged all the time",
                                       "fear being criticised", "avoid eye contact","have low self-esteem", "feeling sick",
                                       "sweating", "trembling", "pounding heartbeat", "palpitations", "have panic attacks",
                                       "have an overwhelming sense of fear and anxiety, usually only for a few minutes"],
                    "Stress": ["headaches", "dizziness", "muscle tension", "pain", "stomach problems", "chest pain",
                               "faster heartbeat", "sexual problems", "difficulty concentrating", "struggling to make decisions",
                               "feeling overwhelmed", "constantly worrying", "being forgetful", "being irritable and snappy",
                               "sleeping too much or too little", "eating too much or too little", "avoiding certain places or people",
                               "drinking or smoking more"]
                    }
    for symptom in symptoms:
        add_symptom("symptom:" + symptom)

    g.serialize(format='pretty-xml', destination=output_path)

