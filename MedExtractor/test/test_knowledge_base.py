import os

from medextractor.knowledge.base import KnowledgeBase
from medextractor.knowledge.entity import EntityType, Entity
from medextractor.knowledge.relations import RelationType
from medextractor.knowledge.semantics import SemanticRelation

print("cwd: " + os.getcwd())
file_name = "knowledgebase.pickle"
knowledge_base_path = os.path.join('../resources', "knowledgebase.pickle")

depression = Entity("depression", EntityType.DISEASE)
lack_of_energy = Entity("lack of energy", EntityType.SYMPTOM)

semantic_relation = SemanticRelation(depression, lack_of_energy, RelationType.HAS_SYMPTOM)
print(str(semantic_relation))

save = True
save = False

knowledge_base = KnowledgeBase()

if save:
    knowledge_base.add_relation(semantic_relation)

    knowledge_base.save(knowledge_base_path)
    # with open(file_name, 'wb') as file:
    #     pickle.dump(knowledge_base, file)

else:
    knowledge_base.load(knowledge_base_path)
    # with open(file_name, 'rb') as file:
    #     knowledge_base = pickle.load(file)

    for relation in knowledge_base.semantic_relations:
        print(relation)

    print()

    print(knowledge_base.has_relation(semantic_relation))


