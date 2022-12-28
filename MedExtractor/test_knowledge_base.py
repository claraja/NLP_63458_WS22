import pickle

from knowledge.base import KnowledgeBase
from knowledge.entity import EntityType, Entity
from knowledge.relations import RelationType
from knowledge.semantics import SemanticRelation

file_name = "knowledgebase.pickle"

depression = Entity("depression", EntityType.DISEASE)
lack_of_energy = Entity("lack of energy", EntityType.SYMPTOM)

semantic_relation = SemanticRelation(depression, lack_of_energy, RelationType.HAS_SYMPTOM)
print(str(semantic_relation))

save = True
save = False

knowledge_base = KnowledgeBase()

if save:
    knowledge_base.add_relation(semantic_relation)

    knowledge_base.save("knowledgebase.pickle")
    # with open(file_name, 'wb') as file:
    #     pickle.dump(knowledge_base, file)

else:
    knowledge_base.load("knowledgebase.pickle")
    # with open(file_name, 'rb') as file:
    #     knowledge_base = pickle.load(file)

    for relation in knowledge_base.semantic_relations:
        print(relation)

    print()

    print(knowledge_base.has_relation(semantic_relation))


