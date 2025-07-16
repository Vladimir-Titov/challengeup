import inspect
import logging
from typing import Any, Dict, List, Optional, Type, get_origin, get_args, Union

from pydantic import BaseModel
from starlette.routing import Route, Mount
from starlette.schemas import BaseSchemaGenerator

from core.web.endpoints.base import BaseEndpoint, EndpointMeta

logger = logging.getLogger(__name__)


class EndpointSchemaGenerator(BaseSchemaGenerator):

    def __init__(self, info: Dict[str, Any]):
        self.info = info

    def get_schema(self, routes: List[Route]) -> Dict[str, Any]:
        """Генерирует OpenAPI схему из маршрутов"""
        openapi_schema = {
            'openapi': '3.0.3',
            'info': self.info,
            'paths': {},
            'components': {
                'schemas': {}
            }
        }

        components = {}

        for route in routes:
            if isinstance(route, Route) and getattr(route, 'include_in_schema', True):
                path_info = self._get_path_info(route, components)
                if path_info:
                    openapi_schema['paths'][route.path] = path_info
            elif isinstance(route, Mount):
                sub_schema = self.get_schema(route.routes)
                for path, path_info in sub_schema.get('paths', {}).items():
                    full_path = route.path.rstrip('/') + path
                    openapi_schema['paths'][full_path] = path_info

                components.update(sub_schema.get('components', {}).get('schemas', {}))

        openapi_schema['components']['schemas'].update(components)

        return openapi_schema

    def _get_path_info(self, route: Route, components: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not hasattr(route, 'endpoint') or not inspect.isclass(route.endpoint):
            return None

        endpoint_class = route.endpoint

        if not issubclass(endpoint_class, BaseEndpoint):
            return None

        path_info = {}

        for method in route.methods or ['GET']:
            if method.upper() in ['HEAD', 'OPTIONS']:
                continue
                
            method_info = self._get_method_info(endpoint_class, method.lower(), components)
            if method_info:
                path_info[method.lower()] = method_info

        return path_info if path_info else None

    def _get_method_info(
        self, endpoint_class: Type[BaseEndpoint], method: str, components: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        
        meta_attr = getattr(endpoint_class, 'meta', EndpointMeta())
        
        if hasattr(meta_attr, 'func'):
            meta = meta_attr()
        elif isinstance(meta_attr, EndpointMeta):
            meta = meta_attr
        else:
            meta = EndpointMeta()
        
        summary = meta.summary or endpoint_class.__name__
        operation_id = meta.operation_id or self._generate_operation_id_from_class_name(endpoint_class.__name__)

        method_info = {
            'summary': summary,
            'operationId': operation_id,
            'responses': {
                '200': {'description': 'Successful response'}
            },
        }

        description = meta.description or self._get_description_from_docstring(endpoint_class)
        if description:
            method_info['description'] = description

        if meta.tag:
            method_info['tags'] = [meta.tag]

        parameters = []
        
        if hasattr(endpoint_class, 'schema_query') and endpoint_class.schema_query:
            query_params = self._get_query_parameters(endpoint_class.schema_query, components)
            parameters.extend(query_params)

        if hasattr(endpoint_class, 'schema_path') and endpoint_class.schema_path:
            path_params = self._get_path_parameters(endpoint_class.schema_path, components)
            parameters.extend(path_params)

        if hasattr(endpoint_class, 'schema_headers') and endpoint_class.schema_headers:
            header_params = self._get_header_parameters(endpoint_class.schema_headers, components)
            parameters.extend(header_params)

        if parameters:
            method_info['parameters'] = parameters

        if (
            hasattr(endpoint_class, 'schema_body')
            and endpoint_class.schema_body
            and method.lower() in ['post', 'put', 'patch']
        ):
            request_body = self._get_request_body(endpoint_class.schema_body, components)
            if request_body:
                method_info['requestBody'] = request_body

        if hasattr(endpoint_class, 'schema_response') and endpoint_class.schema_response:
            response_schema = self._get_response_schema(endpoint_class.schema_response, components)
            if response_schema:
                method_info['responses']['200'] = {
                    'description': 'Successful response',
                    'content': {
                        'application/json': {
                            'schema': response_schema
                        }
                    }
                }

        error_responses = self._get_standard_error_responses(endpoint_class.__name__, method)
        method_info['responses'].update(error_responses)

        return method_info





    def _generate_operation_id_from_class_name(self, class_name: str) -> str:
        """Генерирует operationId из имени класса"""
        if class_name:
            return class_name[0].lower() + class_name[1:]
        return class_name.lower()

    def _get_description_from_docstring(self, endpoint_class: Type[BaseEndpoint]) -> Optional[str]:
        """Извлекает описание из docstring класса"""
        if endpoint_class.__doc__:
            lines = [line.strip() for line in endpoint_class.__doc__.strip().split('\n')]
            while lines and not lines[0]:
                lines.pop(0)
            while lines and not lines[-1]:
                lines.pop()

            if lines:
                return '\n'.join(lines)

        return None

    def _get_standard_error_responses(self, class_name: str, method: str) -> Dict[str, Dict[str, Any]]:
        """Генерирует стандартные error responses на основе типа операции"""
        responses = {}

        if method.lower() in ['post', 'put', 'patch']:
            responses['400'] = {
                'description': 'Ошибка валидации данных',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'code': {'type': 'string'},
                                'message': {'type': 'string'}
                            },
                            'required': ['code', 'message']
                        },
                        'example': {'code': 'validation_error', 'message': 'Validation failed'}
                    }
                },
            }

        # Добавляем 404 для операций с ID
        if 'ByID' in class_name or '{id}' in method:
            resource = class_name.replace('Get', '').replace('Update', '').replace('Delete', '').replace('ByID', '')
            responses['404'] = {
                'description': f'{resource} не найден',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'code': {'type': 'string'},
                                'message': {'type': 'string'}
                            },
                            'required': ['code', 'message']
                        },
                        'example': {'code': 'not_found', 'message': f'{resource} not found'}
                    }
                },
            }

        # Добавляем 409 для Create операций
        if class_name.startswith('Create'):
            responses['409'] = {
                'description': 'Ресурс уже существует',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'code': {'type': 'string'},
                                'message': {'type': 'string'}
                            },
                            'required': ['code', 'message']
                        },
                        'example': {'code': 'already_exists', 'message': 'Resource already exists'}
                    }
                },
            }

        # Добавляем 500 для всех операций
        responses['500'] = {
            'description': 'Внутренняя ошибка сервера',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'code': {'type': 'string'},
                            'message': {'type': 'string'}
                        },
                        'required': ['code', 'message']
                    },
                    'example': {'code': 'internal_server_error', 'message': 'Internal Server Error'}
                }
            }
        }

        return responses

    def _get_query_parameters(self, schema: Type[BaseModel], components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Генерирует query параметры из Pydantic схемы"""
        parameters = []

        for field_name, field_info in schema.model_fields.items():
            param = {
                'name': field_name,
                'in': 'query',
                'required': field_info.is_required(),
                'schema': self._get_field_schema(field_info, components),
            }

            if field_info.description:
                param['description'] = field_info.description

            parameters.append(param)

        return parameters

    def _get_path_parameters(self, schema: Type[BaseModel], components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Генерирует path параметры из Pydantic схемы"""
        parameters = []

        for field_name, field_info in schema.model_fields.items():
            param = {
                'name': field_name,
                'in': 'path',
                'required': True,  # Path параметры всегда обязательны
                'schema': self._get_field_schema(field_info, components),
            }

            if field_info.description:
                param['description'] = field_info.description

            parameters.append(param)

        return parameters

    def _get_header_parameters(self, schema: Type[BaseModel], components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Генерирует header параметры из Pydantic схемы"""
        parameters = []

        for field_name, field_info in schema.model_fields.items():
            param = {
                'name': field_name,
                'in': 'header',
                'required': field_info.is_required(),
                'schema': self._get_field_schema(field_info, components),
            }

            if field_info.description:
                param['description'] = field_info.description

            parameters.append(param)

        return parameters

    def _get_request_body(self, schema: Type[BaseModel], components: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует request body из Pydantic схемы"""
        schema_ref = self._add_schema_to_components(schema, components)

        return {
            'required': True,
            'content': {
                'application/json': {
                    'schema': schema_ref
                }
            }
        }

    def _get_response_schema(self, schema: Type[BaseModel] | type, components: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует response схему"""
        origin = get_origin(schema)
        if origin is list:
            args = get_args(schema)
            if args and inspect.isclass(args[0]) and issubclass(args[0], BaseModel):
                item_schema = self._add_schema_to_components(args[0], components)
                return {
                    'type': 'array',
                    'items': item_schema
                }

        if inspect.isclass(schema) and issubclass(schema, BaseModel):
            return self._add_schema_to_components(schema, components)

        return {'type': 'object'}

    def _get_field_schema(self, field_info, components: Dict[str, Any]) -> Dict[str, Any]:
        """Получает схему для поля"""
        annotation = field_info.annotation

        origin = get_origin(annotation)
        if origin is Union:
            args = get_args(annotation)
            non_none_args = [arg for arg in args if arg != type(None)]
            if non_none_args:
                annotation = non_none_args[0]

        # Базовые типы
        if annotation == str:
            return {'type': 'string'}
        elif annotation == int:
            return {'type': 'integer'}
        elif annotation == float:
            return {'type': 'number'}
        elif annotation == bool:
            return {'type': 'boolean'}
        elif inspect.isclass(annotation) and issubclass(annotation, BaseModel):
            return self._add_schema_to_components(annotation, components)

        return {'type': 'string'}  

    def _add_schema_to_components(self, model: Type[BaseModel], components: Dict[str, Any]) -> Dict[str, Any]:
        schema_name = model.__name__

        if schema_name not in components:
            model_schema = model.model_json_schema()
            
            if '$defs' in model_schema:
                for def_name, def_schema in model_schema['$defs'].items():
                    fixed_def_schema = self._fix_schema_for_openapi(def_schema)
                    components[def_name] = fixed_def_schema
                del model_schema['$defs']
            
            fixed_schema = self._fix_schema_for_openapi(model_schema)
            components[schema_name] = fixed_schema

        return {'$ref': f'#/components/schemas/{schema_name}'}

    def _fix_schema_for_openapi(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(schema, dict):
            fixed_schema = schema.copy()
            
            if 'enum' in fixed_schema and 'type' not in fixed_schema:
                fixed_schema['type'] = 'string'
            
            if 'anyOf' in fixed_schema:
                any_of = fixed_schema['anyOf']
                if len(any_of) == 2:
                    null_item = None
                    other_item = None
                    
                    for item in any_of:
                        if isinstance(item, dict):
                            if item.get('type') == 'null':
                                null_item = item
                            else:
                                other_item = item
                    
                    if null_item and other_item:
                        del fixed_schema['anyOf']
                        fixed_schema.update(other_item)
                        fixed_schema['nullable'] = True
            
            if '$ref' in fixed_schema:
                ref_value = fixed_schema['$ref']
                if '#/$defs/' in ref_value:
                    ref_name = ref_value.split('#/$defs/')[-1]
                    fixed_schema['$ref'] = f'#/components/schemas/{ref_name}'
            
            if 'properties' in fixed_schema:
                fixed_properties = {}
                for prop_name, prop_schema in fixed_schema['properties'].items():
                    fixed_properties[prop_name] = self._fix_schema_for_openapi(prop_schema)
                fixed_schema['properties'] = fixed_properties
            
            if 'items' in fixed_schema:
                fixed_schema['items'] = self._fix_schema_for_openapi(fixed_schema['items'])
            
            if 'additionalProperties' in fixed_schema and isinstance(fixed_schema['additionalProperties'], dict):
                fixed_schema['additionalProperties'] = self._fix_schema_for_openapi(fixed_schema['additionalProperties'])
            
            return fixed_schema
        
        return schema

