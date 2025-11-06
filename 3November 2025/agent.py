from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(
    name="coder",
    system_message="You are a helpful Python coder."
)

user = UserProxyAgent(
    name="charvi",
    human_input_mode="NEVER"
)

user.initiate_chat(assistant, message="Write a Python function to calculate Fibonacci numbers.")
