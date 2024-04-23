from typing import List
from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from app.dependencies.user import get_current_user
from app.services import chatbot_service

router = APIRouter()


class Topic(BaseModel):
    topic: str


class IdeasList(BaseModel):
    ideas: List[str]


class Idea(BaseModel):
    idea: str


# API Endpoints
@router.post("/generate_ideas/")
async def generate_ideas(topic: Topic, user: int = Depends(get_current_user)):
    result = chatbot_service.generate_ideas_from_topic(topic.topic)
    if "Sorry" in result[0]:
        raise HTTPException(status_code=500, detail=result[0])
    return result


@router.post("/combine_ideas/")
async def combine_ideas(ideas: IdeasList, user: int = Depends(get_current_user)):
    result = chatbot_service.combine_ideas(ideas.ideas)
    if "Sorry" in result:
        raise HTTPException(status_code=500, detail=result)
    return result


@router.post("/refine_idea/")
async def refine_idea(idea: Idea, user: int = Depends(get_current_user)):
    result = chatbot_service.refine_idea(idea.idea)
    if "Sorry" in result:
        raise HTTPException(status_code=500, detail=result)
    return result
