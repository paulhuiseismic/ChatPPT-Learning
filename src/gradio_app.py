import os
import sys
import datetime

# Add parent directory to path to import from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import gradio as gr
except ImportError:
    print("ERROR: Gradio is not installed. Please run: pip install gradio")
    sys.exit(1)

try:
    from langchain_core.messages import HumanMessage, SystemMessage
    from azure_openai import chat_model
    LANGCHAIN_AVAILABLE = True
except ImportError:
    print("WARNING: langchain-core is not installed. AI transformation will not work.")
    LANGCHAIN_AVAILABLE = False

try:
    from openai_whisper import transcribe as whisper_transcribe
    WHISPER_AVAILABLE = True
except ImportError:
    print("WARNING: openai_whisper is not available. Audio transcription will not work.")
    WHISPER_AVAILABLE = False

from input_parser import parse_input_text
from ppt_generator import generate_presentation
from layout_manager import LayoutManager
from template_manager import load_template, get_layout_mapping
from config import Config
from logger import LOG


def load_system_prompt():
    """Load the system prompt from prompts/formatter.txt"""
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    prompt_path = os.path.join(project_dir, "prompts", "formatter.txt")

    if not os.path.exists(prompt_path):
        LOG.error(f"Prompt file {prompt_path} does not exist")
        return ""

    with open(prompt_path, "r", encoding='utf-8') as file:
        return file.read()


def transcribe_audio(audio_file, task="transcribe"):
    """Transcribe audio file to text using Whisper"""
    if not WHISPER_AVAILABLE:
        return "❌ Whisper is not available. Please check the installation."

    if not audio_file:
        return ""

    try:
        LOG.info(f"Transcribing audio file: {audio_file}")
        text = whisper_transcribe(audio_file, task)
        LOG.info(f"Transcription complete: {text[:100]}...")
        return text
    except Exception as e:
        LOG.error(f"Error transcribing audio: {str(e)}")
        return f"❌ Error transcribing audio: {str(e)}"


def transform_to_markdown(user_input, chat_history):
    """Transform user input to markdown format using Azure OpenAI"""
    if not LANGCHAIN_AVAILABLE:
        error_msg = "❌ LangChain is not installed. Please run: pip install langchain-openai langchain-core"
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": error_msg})
        return error_msg, chat_history

    try:
        system_prompt = load_system_prompt()

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]

        LOG.info(f"Sending request to Azure OpenAI for markdown transformation")
        response = chat_model.invoke(messages)
        markdown_output = response.content

        LOG.info(f"Received markdown output from Azure OpenAI")

        # Update chat history - using proper message format with role and content
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": markdown_output})

        return markdown_output, chat_history

    except Exception as e:
        LOG.error(f"Error transforming to markdown: {str(e)}")
        error_msg = f"❌ Error: {str(e)}"
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": error_msg})
        return error_msg, chat_history


def generate_ppt_from_markdown(markdown_text):
    """Generate PowerPoint presentation from markdown text"""
    try:
        # Get project root directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)

        # Change to project directory to ensure config and templates are found
        original_dir = os.getcwd()
        os.chdir(project_dir)

        try:
            config = Config()

            # Load the template and get layout mapping
            ppt_template = load_template(config.ppt_template)
            layout_manager = LayoutManager(get_layout_mapping(ppt_template))

            # Parse the markdown text
            powerpoint_data, presentation_title = parse_input_text(markdown_text, layout_manager)

            LOG.info(f"Parsed PowerPoint data structure for: {presentation_title}")

            # Generate unique output filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            # Clean presentation title for filename
            clean_title = "".join(c for c in presentation_title if c.isalnum() or c in (' ', '-', '_')).strip()
            clean_title = clean_title or "presentation"
            output_filename = f"{clean_title}_{timestamp}.pptx"
            output_pptx = os.path.join("output", output_filename)

            # Ensure output directory exists
            os.makedirs("output", exist_ok=True)

            # Generate the presentation
            generate_presentation(powerpoint_data, config.ppt_template, output_pptx)

            LOG.info(f"PowerPoint generated successfully: {output_pptx}")

            # Return absolute path for Gradio to access the file
            abs_output_path = os.path.abspath(output_pptx)

            return abs_output_path, f"✅ PowerPoint generated successfully!\n\nFile: {output_filename}"
        finally:
            # Restore original directory
            os.chdir(original_dir)

    except Exception as e:
        LOG.error(f"Error generating PowerPoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, f"❌ Error generating PowerPoint: {str(e)}"


def process_user_input(user_input, chat_history):
    """Process user input: transform to markdown and generate PPT"""
    if not user_input or not user_input.strip():
        return chat_history, "", None, "Please enter some text first."

    # Step 1: Transform to markdown
    markdown_output, updated_history = transform_to_markdown(user_input, chat_history)

    # Step 2: Generate PowerPoint if markdown was generated successfully
    if not markdown_output.startswith("Error:"):
        ppt_file, status_message = generate_ppt_from_markdown(markdown_output)
        return updated_history, markdown_output, ppt_file, status_message
    else:
        return updated_history, markdown_output, None, "Failed to generate markdown. Please try again."


def create_gradio_interface():
    """Create the Gradio chatbot interface"""

    with gr.Blocks(title="ChatPPT - AI PowerPoint Generator") as demo:
        gr.Markdown(
            """
            # 🎨 ChatPPT - AI PowerPoint Generator
            
            Transform your ideas into professional PowerPoint presentations using AI!
            
            **How it works:**
            1. Enter your content or ideas in natural language
            2. AI transforms it into structured markdown format
            3. PowerPoint is automatically generated from the markdown
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📝 Input")

                # Audio upload section
                with gr.Group():
                    gr.Markdown("#### 🎤 Audio Input (Optional)")
                    audio_input = gr.Audio(
                        sources=["upload", "microphone"],
                        type="filepath",
                        label="Upload audio file or record",
                        visible=WHISPER_AVAILABLE
                    )
                    audio_task = gr.Radio(
                        choices=["transcribe", "translate"],
                        value="transcribe",
                        label="Task",
                        visible=WHISPER_AVAILABLE
                    )
                    transcribe_btn = gr.Button(
                        "🎵 Transcribe Audio",
                        variant="secondary",
                        visible=WHISPER_AVAILABLE
                    )
                    if not WHISPER_AVAILABLE:
                        gr.Markdown("⚠️ *Audio transcription not available. Install required dependencies.*")

                # Text input section
                gr.Markdown("#### ✍️ Text Input")
                user_input = gr.Textbox(
                    label="Enter your content",
                    placeholder="Describe your presentation content here...\n\nExample:\n我想做一个关于人工智能的演讲\n包括AI的定义\nAI的应用领域\nAI的未来发展",
                    lines=10
                )

                with gr.Row():
                    submit_btn = gr.Button("🚀 Generate PowerPoint", variant="primary", size="lg")
                    clear_btn = gr.Button("🗑️ Clear", variant="secondary")

            with gr.Column(scale=1):
                gr.Markdown("### 💬 Chat History")
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=400
                )

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📄 Generated Markdown")
                markdown_output = gr.Textbox(
                    label="Markdown Format",
                    lines=12,
                    interactive=False
                )

            with gr.Column():
                gr.Markdown("### 📊 PowerPoint Output")
                status_output = gr.Textbox(
                    label="Status",
                    lines=3,
                    interactive=False
                )
                ppt_output = gr.File(
                    label="Download PowerPoint",
                    type="filepath"
                )

        # Event handlers
        def clear_all():
            return [], "", "", None, "", None

        def handle_audio_transcription(audio_file, task, current_text):
            """Transcribe audio and append to current text"""
            if not audio_file:
                return current_text

            transcribed_text = transcribe_audio(audio_file, task)

            # Append to existing text if there is any
            if current_text and current_text.strip():
                return current_text + "\n\n" + transcribed_text
            else:
                return transcribed_text

        # Audio transcription handler
        if WHISPER_AVAILABLE:
            transcribe_btn.click(
                fn=handle_audio_transcription,
                inputs=[audio_input, audio_task, user_input],
                outputs=[user_input]
            )

        # PowerPoint generation handler
        submit_btn.click(
            fn=process_user_input,
            inputs=[user_input, chatbot],
            outputs=[chatbot, markdown_output, ppt_output, status_output]
        )

        # Clear all handler
        clear_btn.click(
            fn=clear_all,
            outputs=[chatbot, user_input, markdown_output, ppt_output, status_output, audio_input]
        )

        gr.Markdown(
            """
            ---
            ### 📌 Tips:
            - 🎤 **Audio Input**: Upload an audio file or record using your microphone, then click "Transcribe Audio" to convert it to text
            - ✍️ **Text Input**: You can write in natural language (Chinese or English)
            - 🤖 **AI Processing**: The AI will structure your content into slides
            - 📁 **Output**: Each generated PowerPoint will have a unique timestamp
            - 💾 **Storage**: Check the `output/` folder for all generated presentations
            """
        )

    return demo


if __name__ == "__main__":
    LOG.info("Starting ChatPPT Gradio application...")

    # Create and launch the interface
    demo = create_gradio_interface()
    demo.queue().launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860,
        root_path="/gradio"
    )

