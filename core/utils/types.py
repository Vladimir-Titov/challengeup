from typing import Sequence
from sqlmodel import SQLModel
from pydantic import create_model


def partial_apply(
    model: type[SQLModel],
    only: Sequence[str] | None = None,
    exclude: Sequence[str] | None = None,
) -> SQLModel:
    model_name = model.__name__
    exclude_fields = f'Exclude{"".join([field.capitalize() for field in exclude])}' if exclude else None
    only_fields = f'Only{"".join([field.capitalize() for field in only])}' if only else None
    if only_fields:
        model_name = model_name + f'_{only_fields}'
    if exclude_fields:
        model_name = model_name + f'_{exclude_fields}'

    return create_model(
        model_name,
        __config__=model.__config__,
        **{
            field_name: (field_info.annotation, field_info.default)
            for field_name, field_info in model.model_fields.items()
            if (exclude is None or field_name not in exclude) and (only is None or field_name in only)
        },
    )
