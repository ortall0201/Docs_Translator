from crewai import Crew, Agent, Task
from src.tools.translation import TranslationTool

tool = TranslationTool()

agent = Agent(
    role="Test Agent",
    goal="Run a translation",
    backstory="You're here to help test the CrewAI engine.",
    tools=[tool],
    verbose=True
)

task = Task(
    description="Translate something",
    expected_output="A translation",
    agent=agent,
    input_data={"text": "Hello", "source_lang": "en", "target_lang": "pl"}
)

crew = Crew(agents=[agent], tasks=[task], verbose=True)
print(crew.kickoff())
