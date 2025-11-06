import os
import requests
from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from litellm import completion

# Load API keys from environment
load_dotenv()
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
LLM_API_KEY = os.getenv("OPENAI_API_KEY")

def query_llm(prompt_text: str) -> str:
    """Query LiteLLM for a response"""
    result = completion(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt_text}],
        api_key=LLM_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    return result["choices"][0]["message"]["content"]

# Define the weather specialist agent
forecast_agent = Agent(
    role="Weather Analyst",
    goal="Provide accurate and user-friendly weather updates for any location",
    backstory="An expert in meteorological data interpretation and forecasting trends.",
    verbose=False
)

def get_weather_report(location: str) -> str:
    """Fetch current weather data from OpenWeather API"""
    endpoint = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(endpoint)
        data = response.json()
        if data.get("cod") != 200:
            return f"Unable to find weather data for '{location}'. Try a different city."
        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        return f"Temperature: {temp}°C | Condition: {condition} | Humidity: {humidity}% | Wind Speed: {wind} m/s"
    except Exception as e:
        return f"Error retrieving weather data: {e}"

print("\n=== CrewAI Weather Forecaster ===")

while True:
    user_city = input("Enter a city for weather info (or type 'exit' to quit): ").strip()
    if user_city.lower() == "exit":
        print("Bot: Farewell! Stay weather-aware.")
        break
    print("Bot:", get_weather_report(user_city))

    # Define task for CrewAI agent
    forecast_task = Task(
        description=f"Gather and summarize the latest weather conditions for {user_city}.",
        agent=forecast_agent,
        expected_output="A brief and informative weather update for the user."
    )

    # Assemble and run the crew
    weather_crew = Crew(
        agents=[forecast_agent],
        tasks=[forecast_task]
    )

    print("\nBot:", get_weather_report(user_city))
