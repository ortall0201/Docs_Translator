# src/crew.py - CrewAI agents and tasks with BaseTool subclasses

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

from src.tools.translation import TranslationTool
from src.tools.annotation import AnnotationTool

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Define the LLM
llm = ChatOpenAI(
    model="gpt-4o",   # You can change to "gpt-4" or "gpt-3.5-turbo"
    temperature=0,
    api_key=api_key
)

# Tools
translation_tool = TranslationTool()
annotation_tool = AnnotationTool()

# Agents
FormTranslatorAgent = Agent(
    role="Form Translator",
    goal="Help users understand and fill out foreign bureaucratic forms",
    backstory=(
        "You specialize in translating government and bureaucratic forms into simpler native-language formats, "
        "and provide users with short helpful annotations when fields are unclear."
    ),
    tools=[translation_tool, annotation_tool],
    verbose=True,
    llm=llm
)

ResponseBackTranslatorAgent = Agent(
    role="Response Translator",
    goal="Convert user answers into the correct official language for form submission",
    backstory=(
        "You take filled form responses and translate them back into the original form language in a structured, official tone."
    ),
    tools=[translation_tool],
    verbose=True,
    llm=llm
)

# Tasks
def get_translation_task(text, source_lang, target_lang):
    return Task(
        description="Translate the form and annotate fields for user clarity.",
        expected_output="Translated and annotated form content.",
        agent=FormTranslatorAgent,
        input_data={
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
    )

def get_fill_task(text, source_lang, target_lang):
    return Task(
        description="Translate filled user answers into official language format.",
        expected_output="Translated user responses ready for insertion in the original form.",
        agent=ResponseBackTranslatorAgent,
        input_data={
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
    )

# Crew
def run_crew(mode: str, text: str, source_lang: str, target_lang: str):
    if mode == "translate":
        task = get_translation_task(text, source_lang, target_lang)
    elif mode == "fill":
        task = get_fill_task(text, source_lang, target_lang)
    else:
        raise ValueError("Invalid mode. Use 'translate' or 'fill'")

    crew = Crew(
        agents=[FormTranslatorAgent, ResponseBackTranslatorAgent],
        tasks=[task],
        verbose=True
    )

    return crew.kickoff()
