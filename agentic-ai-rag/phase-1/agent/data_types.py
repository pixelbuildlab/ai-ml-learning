from pydantic import BaseModel


class Memory(BaseModel):
    should_remember: bool
    key: str | None
    value: str | None
