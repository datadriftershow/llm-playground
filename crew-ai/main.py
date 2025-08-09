from crewai import Agent, Task, Crew

# Agents and Crews will automatically use the LLM defined in the
# OPENAI_API_BASE, OPENAI_MODEL_NAME, and OPENAI_API_KEY
# environment variables. No client definition is needed.

# 1. Define your Agent
hello_agent = Agent(
    role='Greeter',
    goal='Be awesome and greet the world with a "Hello, World!" message.',
    backstory='You are a friendly agent, created to say "Hello, World!" in a cheerful way.',
    verbose=True,
    allow_delegation=False,
)

# 2. Define your Task
hello_task = Task(
    description='Create a "Hello, World!" message.',
    expected_output='A string containing the phrase "Hello, World!".',
    agent=hello_agent
)

# 3. Assemble the Crew
hello_crew = Crew(
    agents=[hello_agent],
    tasks=[hello_task],
    verbose=True
)

# 4. Kick off the work
print("######################")
print("Starting the Hello World Crew...")
result = hello_crew.kickoff()

print("######################")
print("Crew Work Complete. Final Result:")
print(result)
