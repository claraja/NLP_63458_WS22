from knowledge.base import KnowledgeBase
from knowledge.entity import EntityType, Entity
from knowledge.relations import RelationType
from knowledge.semantics import SemanticRelation

knowledge_base = KnowledgeBase()

depression = Entity("depression", EntityType.DISEASE)
lack_of_energy = Entity("lack of energy", EntityType.SYMPTOM)

semantic_relation = SemanticRelation(depression, lack_of_energy, RelationType.HAS_SYMPTOM)

knowledge_base.add_relation(semantic_relation)

print(knowledge_base.has_relation(semantic_relation))