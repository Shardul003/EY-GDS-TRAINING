from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(
    name="coder",
    system_message="Hello coder"
)

user = UserProxyAgent(
    name="shardul",
    human_input_mode="NEVER"
)

user.initiate_chat(assistant, message="Write a Python function to calculate Prime numbers.")
