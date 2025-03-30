from typing import List

from pydantic import BaseModel

from at_simulation_api.repository.editor.template.models.models import (
    IrregularEventDB,
    OperationDB,
    RuleDB,
)


class Templates(BaseModel):
    irregular_events: List[IrregularEventDB]
    operations: List[OperationDB]
    rules: List[RuleDB]
