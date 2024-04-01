from pydantic import BaseModel


class SessionBase(BaseModel):
    pass


class SessionCreate(SessionBase):
    project_id: int
    title: str
    description: str
    ideation_technique: str
    session_status: str
    objectives: str


class SessionUpdate(SessionBase):
    title: str
    description: str
    session_status: str
    objectives: str
