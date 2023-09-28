from pydantic import BaseModel


class PostSchemas(BaseModel):
    title: str
    description: str | None = None