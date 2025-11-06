import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
import litellm

# ---------------------------------------------------------------------
# 1. Load API credentials from environment
# ---------------------------------------------------------------------
load_dotenv()
router_api_key = os.getenv("OPENROUTER_API_KEY")

if not router_api_key:
    raise ValueError("OPENROUTER_API_KEY is missing from environment variables")

os.environ["OPENROUTER_API_KEY"] = router_api_key

# ---------------------------------------------------------------------
# 2. Configure LiteLLM for OpenRouter
# ---------------------------------------------------------------------
litellm.api_key = router_api_key
litellm.api_base = "https://openrouter.ai/api/v1"
llm_identifier = "openrouter/mistralai/mistral-7b-instruct"

# ---------------------------------------------------------------------
# 3. Define AI Agents
# ---------------------------------------------------------------------
project_planner = Agent(
    role="Project Planner",
    goal="Design a clear 3-step execution plan with defined goals and deliverables.",
    backstory="An AI strategist skilled in breaking down complex topics into actionable steps.",
    allow_delegation=True,
    llm=llm_identifier,
)

project_executor = Agent(
    role="Execution Specialist",
    goal="Implement the planner’s strategy and summarize the outcomes effectively.",
    backstory="An AI engineer focused on delivering results and reporting progress.",
    llm=llm_identifier,
)

# ---------------------------------------------------------------------
# 4. Define Tasks for Each Agent
# ---------------------------------------------------------------------
planning_task = Task(
    description="Create a 3-step execution plan for the given topic, outlining goals and deliverables.",
    expected_output="Three clearly defined steps, each with a goal and deliverable.",
    agent=project_planner,
)

execution_task = Task(
    description="Summarize the results of the 3-step plan, including what was achieved in each phase.",
    expected_output="A concise 3-point summary of outcomes and progress.",
    agent=project_executor,
)

# ---------------------------------------------------------------------
# 5. Assemble and Run the Crew
# ---------------------------------------------------------------------
workflow_team = Crew(
    agents=[project_planner, project_executor],
    tasks=[planning_task, execution_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    project_topic = "Developing an AI-based document summarization system"
    print(f"\n--- CrewAI Workflow Execution ---\nTopic: {project_topic}\n")
    final_result = workflow_team.kickoff(inputs={"topic": project_topic})
    print("\n--- FINAL OUTPUT ---\n")
    print(final_result)
