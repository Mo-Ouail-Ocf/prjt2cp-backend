import openai
from app.core.config import OPENAI_TOKEN

openai.api_key = OPENAI_TOKEN


def generate_ideas_from_topic(topic: str) -> list[str]:
    try:
        messages = [
            {
                "role": "user",
                "content": f"Generate three concise and innovative and short ideas about: {topic}",
            }
        ]
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )
        return response.choices[0].message.content.strip().split("\n")
    except Exception as e:
        print(f"Error in generating ideas: {str(e)}")
        return ["Sorry, I am unable to generate ideas right now."]


def combine_ideas(ideas: list[str]) -> str:
    try:
        prompt_message = (
            "Combine the following ideas into one concise and short idea: "
            + ", ".join(ideas)
        )
        messages = [{"role": "user", "content": prompt_message}]
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in combining ideas: {str(e)}")
        return "Sorry, I am unable to combine ideas right now."


def refine_idea(idea: str) -> str:
    try:
        messages = [
            {
                "role": "user",
                "content": f"Refine and improve this idea into a concise and short version: {idea}",
            }
        ]
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in refining idea: {str(e)}")
        return "Sorry, I am unable to refine the idea right now."
