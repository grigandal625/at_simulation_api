from typing import List

from sqlalchemy.orm import Session

from at_simulation_api.repository.editor.resource.models.conversions import (
    to_Resource,
    to_ResourceAttribute,
    to_ResourceDB,
    to_ResourceType,
    to_ResourceTypeAttribute,
    to_ResourceTypeDB,
)
from at_simulation_api.repository.editor.resource.models.models import (
    ResourceDB,
    ResourceTypeDB,
)
from at_simulation_api.repository.helper import handle_sqlalchemy_errors
from at_simulation_api.schema.resource import (
    Resource,
    ResourceAttribute,
    ResourceType,
    ResourceTypeAttribute,
)


class ResourceRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @handle_sqlalchemy_errors
    def create_resource_type(self, resource_type: ResourceTypeDB) -> int:
        new_resource_type = to_ResourceType(resource_type)
        self.db_session.add(new_resource_type)
        self.db_session.flush()

        new_resource_types_attributes = [
            to_ResourceTypeAttribute(attr, new_resource_type.id)
            for attr in resource_type.attributes
        ]
        self.db_session.add_all(new_resource_types_attributes)
        return new_resource_type.id

    @handle_sqlalchemy_errors
    def get_resource_type(self, resource_type_id: int) -> ResourceTypeDB:
        resource_type = self._get_resource_type_by_id(resource_type_id)
        if not resource_type:
            raise RuntimeError("Resource type does not exist")
        attributes = self._get_attributes_by_resource_type_id(resource_type_id)
        return to_ResourceTypeDB(resource_type, attributes)

    @handle_sqlalchemy_errors
    def get_resource_types(self, model_id: int) -> List[ResourceTypeDB]:
        resource_types = (
            self.db_session.query(ResourceType)
            .filter(ResourceType.model_id == model_id)
            .all()
        )

        resource_types_db = [
            to_ResourceTypeDB(
                resource_type,
                self._get_attributes_by_resource_type_id(resource_type.id),
            )
            for resource_type in resource_types
        ]
        return resource_types_db

    @handle_sqlalchemy_errors
    def update_resource_type(self, resource_type: ResourceTypeDB) -> int:
        existing_resource_type = self._get_resource_type_by_id(resource_type.id)
        if not existing_resource_type:
            raise RuntimeError("Resource type not found")

        existing_resource_type.name = resource_type.name
        existing_resource_type.type = resource_type.type
        existing_resource_type.model_id = resource_type.model_id

        existing_attributes = {
            attr.id: attr
            for attr in self.db_session.query(ResourceTypeAttribute)
            .filter(ResourceTypeAttribute.resource_type_id == resource_type.id)
            .all()
        }
        existing_attribute_ids = set(existing_attributes.keys())

        for attr in resource_type.attributes:
            if attr.id in existing_attributes:
                existing_attributes[attr.id].name = attr.name
                existing_attributes[attr.id].type = attr.type
                existing_attributes[attr.id].default_value = attr.default_value
                existing_attribute_ids.remove(attr.id)
            else:
                self.db_session.add(to_ResourceTypeAttribute(attr, resource_type.id))

        for attr_id in existing_attribute_ids:
            attr_to_delete = existing_attributes[attr_id]
            self.db_session.delete(attr_to_delete)

        return resource_type.id

    @handle_sqlalchemy_errors
    def delete_resource_type(self, resource_type_id: int) -> int:
        resource_type = self._get_resource_type_by_id(resource_type_id)
        if not resource_type:
            raise RuntimeError("Resource type not found")
        self.db_session.delete(resource_type)

        return resource_type_id

    @handle_sqlalchemy_errors
    def create_resource(self, resource: ResourceDB) -> int:
        new_resource = to_Resource(resource)
        self.db_session.add(new_resource)
        self.db_session.flush()

        new_resource_attributes = [
            to_ResourceAttribute(attr, new_resource.id) for attr in resource.attributes
        ]
        self.db_session.add_all(new_resource_attributes)

        return new_resource.id

    @handle_sqlalchemy_errors
    def get_resource(self, resource_id: int) -> ResourceDB:
        resource = self._get_resource_by_id(resource_id)
        if not resource:
            raise RuntimeError("Resource not found")
        attributes = self._get_attributes_by_resource_id(resource.id)

        return to_ResourceDB(resource, attributes)

    @handle_sqlalchemy_errors
    def get_resources(self, model_id: int) -> List[ResourceDB]:
        resources = (
            self.db_session.query(Resource).filter(Resource.model_id == model_id).all()
        )

        resources_db = [
            to_ResourceDB(resource, self._get_attributes_by_resource_id(resource.id))
            for resource in resources
        ]
        return resources_db

    @handle_sqlalchemy_errors
    def update_resource(self, resource: ResourceDB) -> int:
        existing_resource = self._get_resource_by_id(resource.id)
        if not existing_resource:
            raise RuntimeError("Resource not found")

        existing_resource.name = resource.name
        existing_resource.to_be_traced = resource.to_be_traced
        existing_resource.resource_type_id = resource.resource_type_id
        existing_resource.model_id = resource.model_id

        existing_attributes = {
            attr.id: attr
            for attr in self.db_session.query(ResourceAttribute)
            .filter(ResourceAttribute.resource_id == resource.id)
            .all()
        }

        for attr in resource.attributes:
            if attr.id in existing_attributes:
                existing_attributes[attr.id].value = attr.value
            else:
                raise RuntimeError("Resource attribute not found")

        return resource.id

    @handle_sqlalchemy_errors
    def delete_resource(self, resource_id: int) -> int:
        resource = self._get_resource_by_id(resource_id)
        if not resource:
            raise RuntimeError("Resource not found")
        self.db_session.delete(resource)

        return resource_id

    def _get_resource_by_id(self, resource_id: int) -> Resource:
        resource = (
            self.db_session.query(Resource).filter(Resource.id == resource_id).first()
        )
        if not resource:
            raise ValueError("Resource does not exist")
        return resource

    def _get_resource_type_by_id(self, resource_type_id: int) -> ResourceType:
        resource_type = (
            self.db_session.query(ResourceType)
            .filter(ResourceType.id == resource_type_id)
            .first()
        )
        if not resource_type:
            raise ValueError("Resource type does not exist")
        return resource_type

    def _get_attributes_by_resource_id(
        self, resource_id: int
    ) -> List[ResourceAttribute]:
        return (
            self.db_session.query(ResourceAttribute)
            .filter(ResourceAttribute.resource_id == resource_id)
            .all()
        )

    def _get_attributes_by_resource_type_id(
        self, resource_type_id: int
    ) -> List[ResourceTypeAttribute]:
        return (
            self.db_session.query(ResourceTypeAttribute)
            .filter(ResourceTypeAttribute.resource_type_id == resource_type_id)
            .all()
        )
