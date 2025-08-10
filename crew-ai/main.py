import os
from crewai import Agent, Task, Crew
# Import the necessary tool from langchain_community
from langchain_community.tools import DuckDuckGoSearchRun
# Import the 'tool' decorator
from crewai.tools import tool

# You will need to set your OPENAI_API_KEY environment variable.
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# 1. Create a custom tool using the @tool decorator
@tool("DuckDuckGo Search")
def search_tool(query: str) -> str:
    """A wrapper around DuckDuckGo Search. Useful for when you need to answer questions about current events. Input should be a search query."""
    return DuckDuckGoSearchRun().run(query)

# 2. Define your Agents
# We will create two agents: a researcher and a writer.

# Agent 1: The Researcher
# This agent is responsible for searching the web for information.
researcher_agent = Agent(
    role='Senior Tech History Researcher',
    goal='Uncover the origin story of the "Hello, World!" program',
    backstory=(
        "You are an expert in the history of computer science. "
        "You are skilled at using web search tools to find "
        "accurate and interesting information from the early days of computing."
    ),
    verbose=True,
    allow_delegation=False,
    # Assign the decorated function as the tool
    tools=[search_tool],
    # Enable memory for the agent
    memory=True
)

# Agent 2: The Writer
# This agent is responsible for taking the research and writing a compelling story.
writer_agent = Agent(
    role='Engaging Tech Content Writer',
    goal='Write a short, fun blog post about the origin of "Hello, World!"',
    backstory=(
        "You are a talented writer who can take factual information "
        "and turn it into a captivating story. You specialize in making "
        "tech history accessible and exciting for a general audience."
    ),
    verbose=True,
    allow_delegation=False,
    # Enable memory for the agent
    memory=True
)

# 3. Define your Tasks
# We need two tasks, one for each agent.

# Task 1: The Research Task
# This task will be performed by the researcher_agent.
research_task = Task(
    description=(
        "Search the web to find the origin of the 'Hello, World!' program. "
        "Identify who wrote it, in what programming language, "
        "and for which computer or documentation it was first intended. "
        "Your final answer must be a summary of these findings."
    ),
    expected_output=(
        "A concise summary in a paragraph, detailing the creator, "
        "language, and the original context of the 'Hello, World!' program."
    ),
    agent=researcher_agent
)

# Task 2: The Writing Task
# This task will be performed by the writer_agent. It uses the output
# of the research_task as its context.
writing_task = Task(
    description=(
        "Using the research findings about the origin of 'Hello, World!', "
        "write a short and cheerful blog post. The tone should be fun and "
        "engaging, aimed at people new to programming."
    ),
    expected_output=(
        "A 2-paragraph blog post. The first paragraph should cheerfully "
        "introduce the 'Hello, World!' tradition, and the second should "
        "explain its interesting origin story."
    ),
    agent=writer_agent,
    # The 'context' parameter tells this task to use the output of another task.
    context=[research_task]
)

# 4. Assemble the Crew
# Create the crew with the defined agents and tasks.
# The tasks will be executed sequentially by default.
hello_world_crew = Crew(
    agents=[researcher_agent, writer_agent],
    tasks=[research_task, writing_task],
    verbose=True
)

# 5. Kick off the work
print("######################")
print("Starting the Enhanced 'Hello, World!' Crew...")
result = hello_world_crew.kickoff()

print("######################")
print("Crew Work Complete. Final Result:")
print(result)
