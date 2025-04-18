from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel


class BaseTypesEnum(Enum):
    INT = "INT"
    FLOAT = "FLOAT"
    BOOL = "BOOL"
    ENUM = "ENUM"


class ResourceTypeAttributeRequest(BaseModel):
    id: Optional[int] = None
    name: str
    type: BaseTypesEnum
    enum_values_set: Optional[List[str]] = None
    default_value: Optional[Union[int, float, bool, str]] = None


class ResourceTypeAttributeResponse(ResourceTypeAttributeRequest):
    id: int


class ResourceTypeTypesEnum(Enum):
    CONSTANT = "CONSTANT"
    TEMPORAL = "TEMPORAL"


class ResourceTypeRequest(BaseModel):
    id: Optional[int] = None
    name: str
    type: ResourceTypeTypesEnum
    attributes: List[ResourceTypeAttributeRequest]


class ResourceTypeResponse(ResourceTypeRequest):
    id: int
    attributes: List[ResourceTypeAttributeResponse]


class ResourceTypesResponse(BaseModel):
    resource_types: List[ResourceTypeResponse]
    total: int


class ResourceAttributeRequest(BaseModel):
    id: Optional[int] = None
    rta_id: int
    value: Optional[Union[int, float, bool, str]] = None


class ResourceAttributeResponse(ResourceAttributeRequest):
    id: int


class ResourceRequest(BaseModel):
    id: Optional[int] = None
    name: str
    to_be_traced: bool
    attributes: List[ResourceAttributeRequest]
    resource_type_id: int


class ResourceResponse(ResourceRequest):
    id: int
    attributes: List[ResourceAttributeResponse]


class ResourcesResponse(BaseModel):
    resources: List[ResourceResponse]
    total: int
