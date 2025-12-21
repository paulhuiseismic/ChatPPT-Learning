from abc import ABC, abstractmethod

from azure_openai import chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory

from logger import LOG
from chat_history import get_session_history


class ChatBot(ABC):
    def __init__(self, prompt_file="./prompts/chatbot.txt", session_id=None):
        self.chatbot = None
        self.chatbot_with_history = None
        self.prompt_file = prompt_file
        self.session_id = session_id if session_id else "default_session_id"
        self.prompt = self.load_prompt()
        self.create_chatbot()  # Initialize the chatbot automatically

    def load_prompt(self):
        """Load the prompt template from a file."""
        try:
            with open(self.prompt_file, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {self.prompt_file}")

    def create_chatbot(self):
        system_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.prompt),
                MessagesPlaceholder(variable_name="messages")
            ]
        )

        self.chatbot = system_prompt | chat_model

        self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot, get_session_history)

    def chat_with_history(self, user_input, session_id=None):
        if session_id is None:
            session_id = self.session_id

        response = self.chatbot_with_history.invoke(
            [HumanMessage(content=user_input)],
            {"configurable": {"session_id": session_id}},
        )

        LOG.debug(f"[chatbot] {response.content}")
        return response.content