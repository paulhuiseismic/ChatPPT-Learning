"""
Reflection-based chatbot using LangGraph for high-quality content generation.
This module implements a generate-reflect cycle to iteratively improve markdown content.
"""

from typing import TypedDict, Annotated, List, Tuple
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from azure_openai import chat_model
from logger import LOG


class ReflectionState(TypedDict):
    """State for the reflection graph"""
    messages: Annotated[list, add_messages]
    reflection_count: int
    feedbacks: List[str]  # Store feedback from each reflection round


class ReflectionChatBot:
    """
    A chatbot that uses reflection mechanism to generate high-quality content.
    It generates content, reflects on it, and iteratively improves it.
    """

    MAX_REFLECTION_ROUNDS = 3  # Limit reflection to 3 rounds

    def __init__(self, prompt_file: str, session_id: str = None):
        """
        Initialize the reflection chatbot.

        Args:
            prompt_file: Path to the system prompt file for content generation
            session_id: Session identifier for maintaining conversation context
        """
        self.prompt_file = prompt_file
        self.session_id = session_id or "default_session"
        self.generation_prompt = self._load_prompt()
        self.reflection_prompt = self._create_reflection_prompt()

        # Create the LangChain chains
        self.generator = self._create_generator()
        self.reflector = self._create_reflector()

        # Build the reflection graph
        self.graph = self._build_graph()

    def _load_prompt(self) -> str:
        """Load the system prompt from file"""
        try:
            with open(self.prompt_file, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            LOG.error(f"Prompt file not found: {self.prompt_file}")
            raise FileNotFoundError(f"Prompt file not found: {self.prompt_file}")

    def _create_reflection_prompt(self) -> str:
        """Create the reflection prompt for critiquing content"""
        return (
            "You are a reviewer tasked with providing constructive critique and improvement suggestions "
            "for the user's markdown content submission. "
            "Offer detailed feedback, including recommendations on:\n"
            "- Clarity and coherence of the content\n"
            "- Structure and organization of slides\n"
            "- Content depth and completeness\n"
            "- Style and presentation quality\n"
            "- Areas that need expansion or improvement\n\n"
            "Provide specific, actionable suggestions that can be used to improve the content."
        )

    def _create_generator(self):
        """Create the content generation chain"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.generation_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])
        return prompt | chat_model

    def _create_reflector(self):
        """Create the reflection/critique chain"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.reflection_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])
        return prompt | chat_model

    async def _generation_node(self, state: ReflectionState) -> ReflectionState:
        """
        Generation node: Generate or refine content based on user request and feedback.
        """
        current_count = state.get('reflection_count', 0)
        LOG.info(f"Generation round {current_count + 1}")

        # Invoke the generator with current messages
        response = await self.generator.ainvoke(state['messages'])

        # Return updated state - increment reflection_count after generation
        return {
            "messages": [response],
            "reflection_count": current_count,  # Don't increment here, increment in reflection
            "feedbacks": state.get('feedbacks', [])
        }

    async def _reflection_node(self, state: ReflectionState) -> ReflectionState:
        """
        Reflection node: Critique the generated content and provide feedback.
        """
        current_count = state.get('reflection_count', 0)
        LOG.info(f"Reflection round {current_count + 1}")

        # Transform messages for reflection
        # Keep the original user request, but swap AI/Human roles for reflection
        cls_map = {"ai": HumanMessage, "human": AIMessage}

        # First message is the original user request, rest are conversation history
        transformed = [state['messages'][0]] + [
            cls_map[msg.type](content=msg.content)
            for msg in state['messages'][1:]
        ]

        # Get reflection/critique
        reflection = await self.reflector.ainvoke(transformed)

        # Update reflection count and store feedback
        feedbacks = state.get('feedbacks', []).copy()
        feedbacks.append(reflection.content)

        return {
            "messages": [HumanMessage(content=reflection.content)],
            "reflection_count": current_count + 1,  # Increment after reflection
            "feedbacks": feedbacks
        }

    def _should_continue(self, state: ReflectionState) -> str:
        """
        Decide whether to continue reflection or end.
        Stop if we've reached max reflection rounds.
        """
        reflection_count = state.get('reflection_count', 0)

        LOG.info(f"Checking continuation: reflection_count={reflection_count}, max={self.MAX_REFLECTION_ROUNDS}")

        # Check if we've reached the maximum reflection rounds
        if reflection_count >= self.MAX_REFLECTION_ROUNDS:
            LOG.info(f"Reached maximum reflection rounds ({self.MAX_REFLECTION_ROUNDS})")
            return END

        # Continue reflection
        return "reflect"

    def _build_graph(self):
        """Build the LangGraph reflection graph"""
        # Create the state graph
        builder = StateGraph(ReflectionState)

        # Add nodes
        builder.add_node("generate", self._generation_node)
        builder.add_node("reflect", self._reflection_node)

        # Add edges
        builder.add_edge(START, "generate")
        builder.add_conditional_edges("generate", self._should_continue)
        builder.add_edge("reflect", "generate")

        # Compile with memory
        memory = MemorySaver()
        return builder.compile(checkpointer=memory)

    async def generate_with_reflection(
        self,
        user_input: str,
        session_id: str = None
    ) -> Tuple[str, List[str]]:
        """
        Generate content with reflection mechanism.

        Args:
            user_input: The user's request/prompt
            session_id: Session identifier

        Returns:
            Tuple of (final_content, list_of_feedbacks)
        """
        session_id = session_id or self.session_id

        # Initial state
        inputs = {
            "messages": [HumanMessage(content=user_input)],
            "reflection_count": 0,
            "feedbacks": []
        }

        config = {"configurable": {"thread_id": session_id}}

        # Run the graph
        final_state = None
        event_count = 0
        try:
            LOG.info("Starting graph execution...")
            async for event in self.graph.astream(inputs, config):
                event_count += 1
                LOG.info(f"Event {event_count}: {list(event.keys())}")

                # Keep track of the latest state
                if 'generate' in event:
                    final_state = event['generate']
                    LOG.info(f"Generation step: {len(event['generate']['messages'])} messages, reflection_count={event['generate'].get('reflection_count', 0)}, feedbacks={len(event['generate'].get('feedbacks', []))}")
                elif 'reflect' in event:
                    final_state = event['reflect']
                    LOG.info(f"Reflection step: {len(event['reflect']['messages'])} messages, reflection_count={event['reflect'].get('reflection_count', 0)}, feedbacks={len(event['reflect'].get('feedbacks', []))}")
                elif '__end__' in event:
                    LOG.info("Graph reached END")

            LOG.info(f"Graph execution completed. Total events: {event_count}")
        except Exception as e:
            LOG.error(f"Error in reflection graph: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

        # Extract final content and feedbacks
        if final_state:
            # The last AI message contains the final generated content
            final_content = None
            for msg in reversed(final_state['messages']):
                if isinstance(msg, AIMessage):
                    final_content = msg.content
                    break

            feedbacks = final_state.get('feedbacks', [])
            LOG.info(f"Extracted final content ({len(final_content) if final_content else 0} chars) and {len(feedbacks)} feedbacks")

            return final_content or "", feedbacks

        LOG.warning("No final state found!")
        return "", []

    def chat_with_reflection(self, user_input: str, session_id: str = None) -> Tuple[str, List[str]]:
        """
        Synchronous wrapper for generate_with_reflection.

        Args:
            user_input: The user's request/prompt
            session_id: Session identifier

        Returns:
            Tuple of (final_content, list_of_feedbacks)
        """
        import asyncio

        # Get or create event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Run the async function
        return loop.run_until_complete(
            self.generate_with_reflection(user_input, session_id)
        )

