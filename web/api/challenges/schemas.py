from pydantic import BaseModel


class GetChallengesQuery(BaseModel):
    title: str | None = None
    order_by: str | None = None
