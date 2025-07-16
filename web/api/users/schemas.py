from pydantic import BaseModel


class GetUsersQuery(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    order_by: str | None = None
