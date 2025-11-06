import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
import litellm

# ---------------------------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------------------------
load_dotenv()
openrouter_key = os.getenv("OPENROUTER_API_KEY")

if not openrouter_key:
    raise ValueError("OPENROUTER_API_KEY not found in environment")

os.environ["OPENROUTER_API_KEY"] = openrouter_key

# ---------------------------------------------------------------------
# 2. Configure LiteLLM for OpenRouter
# ---------------------------------------------------------------------
litellm.api_key = openrouter_key
litellm.api_base = "https://openrouter.ai/api/v1"
llm_model = "openrouter/mistralai/mistral-7b-instruct"

# ---------------------------------------------------------------------
# 3. Define Agents
# ---------------------------------------------------------------------
marketing_planner = Agent(
    role="Marketing Planner",
    goal="Design a 3-step marketing plan with objectives, target audience, and strategies.",
    backstory="A visionary strategist skilled in creating impactful marketing campaigns.",
    allow_delegation=True,
    llm=llm_model,
)

marketing_executor = Agent(
    role="Marketing Specialist",
    goal="Implement the planner’s strategy and summarize campaign results with key metrics.",
    backstory="An analytical marketer focused on execution and performance measurement.",
    llm=llm_model,
)

# ---------------------------------------------------------------------
# 4. Define Tasks
# ---------------------------------------------------------------------
planning_task = Task(
    description="Create a 3-step marketing campaign plan for a given product or service, including objectives, target audience, and strategies.",
    expected_output="A structured plan with 3 steps, each detailing objective, audience, and strategy.",
    agent=marketing_planner,
)

execution_task = Task(
    description="Summarize the outcomes of the marketing plan, including engagement and ROI metrics for each step.",
    expected_output="A 3-point summary of campaign results with performance metrics.",
    agent=marketing_executor,
)

# ---------------------------------------------------------------------
# 5. Create and Run the Crew
# ---------------------------------------------------------------------
crew_team = Crew(
    agents=[marketing_planner, marketing_executor],
    tasks=[planning_task, execution_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    campaign_topic = "Launching a new line of eco-friendly skincare products"
    print(f"\n--- CrewAI Marketing Workflow ---\nTopic: {campaign_topic}\n")
    final_output = crew_team.kickoff(inputs={"topic": campaign_topic})
    print("\n--- FINAL OUTPUT ---\n")
    print(final_output)
