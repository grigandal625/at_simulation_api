from jinja2 import Environment, FileSystemLoader, Template

from at_simulation_api.service.model.models.models import Model
from at_simulation_api.service.translator.function import trnsl_functions
from at_simulation_api.service.translator.irregular_event import trnsl_irregular_events
from at_simulation_api.service.translator.operation import trnsl_operations
from at_simulation_api.service.translator.resource import trnsl_resources
from at_simulation_api.service.translator.resource_type import trnsl_resource_types
from at_simulation_api.service.translator.rule import trnsl_rules
from at_simulation_api.service.translator.template_usage import trnsl_template_usages

TEMPLATE_DIR = "./at_simulation_api/service/translator/templates/"
TEMPLATE_NAME = "main.jinja"

current_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)
template: Template = current_env.get_template(TEMPLATE_NAME)


def trnsl_model(model: Model) -> str:
    resource_types = trnsl_resource_types(model.resource_types)
    resources = trnsl_resources(model.resources, model.resource_types)
    functions = trnsl_functions(model.functions)
    rules = trnsl_rules(model.rules, model.resource_types)
    operations = trnsl_operations(model.operations, model.resource_types)
    irregular_events = trnsl_irregular_events(
        model.irregular_events, model.resource_types
    )

    metas = []
    metas.extend([template.meta for template in model.irregular_events])
    metas.extend([template.meta for template in model.operations])
    metas.extend([template.meta for template in model.rules])
    metas = sorted(metas, key=lambda metas: metas.name)
    template_usages = trnsl_template_usages(
        model.template_usages, metas, model.resources
    )

    rendered_template = template.render(
        resource_types=resource_types,
        resources=resources,
        functions=functions,
        rules=rules,
        operations=operations,
        irregular_events=irregular_events,
        template_usages=template_usages,
    )

    return rendered_template
