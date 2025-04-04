from typing import List

from sqlalchemy.orm import Session

from at_simulation_api.repository.editor.function.models.conversions import (
    to_Function,
    to_FunctionDB,
    to_FunctionParameter,
)
from at_simulation_api.repository.editor.function.models.models import FunctionDB
from at_simulation_api.repository.helper import handle_sqlalchemy_errors
from at_simulation_api.schema.function import Function, FunctionParameter


class FunctionRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @handle_sqlalchemy_errors
    def create_function(self, function: FunctionDB) -> int:
        new_function = to_Function(function)

        self.db_session.add(new_function)
        self.db_session.flush()

        new_function_parameters = [
            to_FunctionParameter(param, new_function.id) for param in function.params
        ]

        self.db_session.add_all(new_function_parameters)

        return new_function.id

    @handle_sqlalchemy_errors
    def get_function(self, function_id: int) -> FunctionDB:
        function = self._get_function_by_id(function_id)
        if not function:
            raise RuntimeError("Function not found")
        parameters = self._get_parameters_by_function_id(function_id)
        return to_FunctionDB(function, parameters)

    @handle_sqlalchemy_errors
    def get_functions(self, model_id: int) -> List[FunctionDB]:
        functions = (
            self.db_session.query(Function).filter(Function.model_id == model_id).all()
        )

        functions_db = [
            to_FunctionDB(function, self._get_parameters_by_function_id(function.id))
            for function in functions
        ]
        return functions_db

    @handle_sqlalchemy_errors
    def update_function(self, function: FunctionDB) -> int:
        existing_function = self._get_function_by_id(function.id)
        if not existing_function:
            raise RuntimeError("Function not found")

        existing_function.name = function.name
        existing_function.ret_type = function.ret_type
        existing_function.body = function.body
        existing_function.model_id = function.model_id

        existing_parameters = {
            param.id: param
            for param in self.db_session.query(FunctionParameter)
            .filter(FunctionParameter.function_id == function.id)
            .all()
        }
        existing_parameter_ids = set(existing_parameters.keys())

        for param in function.params:
            if param.id in existing_parameters:
                existing_parameters[param.id].name = param.name
                existing_parameters[param.id].type = param.type
                existing_parameter_ids.remove(param.id)
            else:
                self.db_session.add(to_FunctionParameter(param, function.id))

        for param_id in existing_parameter_ids:
            param_to_delete = existing_parameters[param_id]
            self.db_session.delete(param_to_delete)

        return function.id

    @handle_sqlalchemy_errors
    def delete_function(self, function_id: int) -> int:
        function = self._get_function_by_id(function_id)
        if not function:
            raise RuntimeError("Function not found")
        self.db_session.delete(function)

        return function_id

    def _get_function_by_id(self, function_id: int) -> Function:
        function = (
            self.db_session.query(Function).filter(Function.id == function_id).first()
        )
        if not function:
            raise ValueError("Function does not exist")
        return function

    def _get_parameters_by_function_id(
        self, function_id: int
    ) -> List[FunctionParameter]:
        return (
            self.db_session.query(FunctionParameter)
            .filter(FunctionParameter.function_id == function_id)
            .all()
        )
