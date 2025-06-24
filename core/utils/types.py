from typing import Sequence, cast, Any
from sqlmodel import SQLModel
from pydantic import BaseModel, create_model


def partial_apply(
    model: type[BaseModel],
    only: Sequence[str] | None = None,
    exclude: Sequence[str] | None = None,
) -> type[BaseModel]:
    model_name = model.__name__
    exclude_fields = f'Exclude{"".join([field.capitalize() for field in exclude])}' if exclude else None
    only_fields = f'Only{"".join([field.capitalize() for field in only])}' if only else None
    if only_fields:
        model_name = model_name + only_fields
    if exclude_fields:
        model_name = model_name + exclude_fields

    return create_model(  # type: ignore
        model_name,
        __config__=model.model_config,
        __base__=model,
        **{
            field_name: (field_info.annotation, field_info.default)
            for field_name, field_info in model.model_fields.items()
            if (exclude is None or field_name not in exclude) and (only is None or field_name in only)
        },
    )
