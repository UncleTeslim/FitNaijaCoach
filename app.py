from langchain.prompts import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import chain
import os
import gradio as gr
from dotenv import load_dotenv
from langchain_community.cache import InMemoryCache
from langchain.globals import set_llm_cache

set_llm_cache(InMemoryCache())

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def load_context(file_path):
    with open(file_path, 'r') as file:
        return file.read()

context_file = "fit.md"
context = load_context(context_file)
# system_prompt_file = "system.md"
# system_prompt = load_context(system_prompt_file)

system_prompt = """You're FitNaijaCoach, a Nigerian fitness expert. ONLY answer fitness/nutrition questions. Adapt responses to the user's goal:

- Lose weight: Focus on cardio, portion control, low-calorie foods, light strength.
- Gain weight: Emphasize nutrient-dense foods, moderate strength, more meals.
- Build muscle: Prioritize strength training, progressive overload, protein, rest.
  Suggest both home and gym workouts unless specified. Use mostly (80%) realistic Nigerian meals. Consider body types, habits, lifestyle, climate. Be clear and empathetic.
  
Focus 80% of your food suggestions on realistic Nigerian meals using common
ingredients (e.g., beans, yam, eba, plantain, moi moi, okra, catfish, turkey, eggs).
Only infuse 20% Western meal ideas (e.g., oats, smoothies, Greek yogurt, chicken salad, quinoa)
where appropriate, or if helpful for the user's fitness goal. Remind user of portion control and moderation when necessary.
  
Consider Nigerian body types, cultural habits, daily lifestyle (e.g., access to fresh markets,
busy work-life), and climate. Speak clearly, practically, and empathetically..
  """




prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt + "\n\n Use the following information to answer the user's questions:\n\n{context}"),
    MessagesPlaceholder(variable_name="messages") 
])


llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.2,
    timeout=None,
    max_retries=2,
    max_tokens = 1000,
    # other params...
)


chain = prompt | llm

# message = HumanMessage(content="How do i get fit as a 30 year old man? suggest workout routines and food plan")
# response = chain.invoke({"context": context, "messages": [message]})
# print(response.content)

def respond(user_message):
    message = HumanMessage(content=user_message)
    response = chain.invoke({"context": context, "messages": [message]})
    return response.content

iface = gr.Interface(
    fn=respond,
    inputs=[gr.Textbox(label="User Message")],
    outputs=gr.Textbox(label="Response"),
    title="FitNaijaCoach",
    description="Ask questions about fitness and get personalized responses.",
    theme="default"
)


if __name__ == "__main__":
    iface.launch(share=True, debug=True, server_port=7860)
                   

# from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage
# import os
# import gradio as gr
# from dotenv import load_dotenv
# from langchain_community.cache import InMemoryCache
# from langchain.globals import set_llm_cache

# # Set cache
# set_llm_cache(InMemoryCache())

# # Retrieve OpenAI API key from environment variables

# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY is not set!")

# # Load context for the model
# def load_context(file_path):
#     with open(file_path, 'r') as file:
#         return file.read()

# context_file = "fit.md"
# context = load_context(context_file)

# # System message for the assistant
# system_prompt = """You're FitNaijaCoach, a Nigerian fitness expert. ONLY answer fitness/nutrition questions. Adapt responses to the user's goal:
# - Lose weight: Focus on cardio, portion control, low-calorie foods, light strength.
# - Gain weight: Emphasize nutrient-dense foods, moderate strength, more meals.
# - Build muscle: Prioritize strength training, progressive overload, protein, rest.
# Focus 80% of your food suggestions on realistic Nigerian meals using common ingredients (e.g., beans, yam, eba, plantain, moi moi, okra, catfish, turkey, eggs).
# Remind user of portion control and moderation when necessary.
# """

# # Build prompt template
# prompt = ChatPromptTemplate.from_messages([
#     ("system", system_prompt + "\n\n Use the following information to answer the user's questions:\n\n{context}"),
#     MessagesPlaceholder(variable_name="messages")
# ])

# # Initialize the LLM
# llm = ChatOpenAI(
#     model="gpt-3.5-turbo",
#     temperature=0.2,
#     timeout=None,
#     max_retries=2,
#     max_tokens=1000,
# )

# # Create the chain
# chain = prompt | llm

# # Function to respond to user messages
# def respond(user_message):
#     try:
#         message = HumanMessage(content=user_message)
#         response = chain.invoke({"context": context, "messages": [message]})
#         return response.content
#     except Exception as e:
#         return f"Error: {str(e)}"

# # Gradio interface setup
# iface = gr.Interface(
#     fn=respond,
#     inputs=[gr.Textbox(label="User Message")],
#     outputs=gr.Textbox(label="Response"),
#     title="FitNaijaCoach",
#     description="Ask questions about fitness and get personalized responses.",
#     theme="default"
# )

# # Run the app
# if __name__ == "__main__":
#     iface.launch(debug=True, server_port=8501)
