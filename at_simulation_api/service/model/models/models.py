from typing import List

from pydantic import BaseModel

from at_simulation_api.repository.editor.function.models.models import FunctionDB
from at_simulation_api.repository.editor.resource.models.models import (
    ResourceDB,
    ResourceTypeDB,
)
from at_simulation_api.repository.editor.template.models.models import (
    IrregularEventDB,
    OperationDB,
    RuleDB,
    TemplateUsageDB,
)
from at_simulation_api.repository.model.models.models import ModelMetaDB


class Model(BaseModel):
    meta: ModelMetaDB
    resource_types: List[ResourceTypeDB]
    resources: List[ResourceDB]
    irregular_events: List[IrregularEventDB]
    operations: List[OperationDB]
    rules: List[RuleDB]
    template_usages: List[TemplateUsageDB]
    functions: List[FunctionDB]
