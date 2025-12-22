import os
import sys
import datetime
import uuid

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
    from chatbot import ChatBot
    from reflection_chatbot import ReflectionChatBot
    from image_advisor import ImageAdvisor
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

# Global instances for chatbot and image advisor with session management
chatbot_instances = {}
image_advisor_instance = None


def get_chatbot_instance(session_id):
    """Get or create a ReflectionChatBot instance for the given session"""
    if session_id not in chatbot_instances:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        prompt_path = os.path.join(project_dir, "prompts", "content_assistant.txt")
        chatbot_instances[session_id] = ReflectionChatBot(prompt_file=prompt_path, session_id=session_id)
    return chatbot_instances[session_id]


def get_image_advisor_instance():
    """Get or create the ImageAdvisor instance"""
    global image_advisor_instance
    if image_advisor_instance is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        prompt_path = os.path.join(project_dir, "prompts", "image_advisor.txt")
        image_advisor_instance = ImageAdvisor(prompt_file=prompt_path)
    return image_advisor_instance


def load_system_prompt():
    """Load the system prompt from prompts/content_assistant.txt"""
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    prompt_path = os.path.join(project_dir, "prompts", "content_assistant.txt")

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


def chat_with_bot(user_input, chat_history, session_id):
    """Chat with the bot to refine markdown content using ReflectionChatBot with reflection mechanism"""
    if not LANGCHAIN_AVAILABLE:
        error_msg = "❌ LangChain is not installed. Please run: pip install langchain-openai langchain-core langgraph"
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": error_msg})
        return chat_history, "", ""

    try:
        # Get chatbot instance for this session
        chatbot = get_chatbot_instance(session_id)

        LOG.info(f"Sending message to reflection chatbot for session {session_id}")

        # Use reflection mechanism to generate high-quality content
        response, feedbacks = chatbot.chat_with_reflection(user_input, session_id)

        LOG.info(f"Received response from reflection chatbot with {len(feedbacks)} feedback rounds")

        # Format feedback for display
        feedback_display = ""
        if feedbacks:
            feedback_display = "### 🔄 Reflection Feedback:\n\n"
            for i, feedback in enumerate(feedbacks, 1):
                feedback_display += f"**Round {i} Feedback:**\n{feedback}\n\n"

        # Update chat history
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response})

        return chat_history, response, feedback_display

    except Exception as e:
        LOG.error(f"Error in chat: {str(e)}")
        import traceback
        traceback.print_exc()
        error_msg = f"❌ Error: {str(e)}"
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": error_msg})
        return chat_history, error_msg, ""


def enhance_markdown_with_images(markdown_text, session_id):
    """Enhance markdown content with images using ImageAdvisor"""
    if not markdown_text or not markdown_text.strip():
        return markdown_text, "⚠️ Please create some content first by chatting with the AI."

    try:
        LOG.info(f"Enhancing markdown with images for session {session_id}")

        # Get image advisor instance
        advisor = get_image_advisor_instance()

        # Generate images and insert into markdown
        enhanced_content, image_pair = advisor.generate_images(
            markdown_text,
            image_directory=f"session_{session_id}",
            num_images=3
        )

        LOG.info(f"Successfully enhanced markdown with {len(image_pair)} images")

        if len(image_pair) > 0:
            status_msg = f"✅ Successfully added {len(image_pair)} images to your presentation!\n"
            status_msg += f"📁 Images saved to: images/session_{session_id}/\n"
            status_msg += "🎨 Markdown has been updated with image references."
        else:
            status_msg = "⚠️ No images were added. The slides may not have suitable content for images."

        return enhanced_content, status_msg

    except Exception as e:
        LOG.error(f"Error enhancing markdown with images: {str(e)}")
        import traceback
        traceback.print_exc()
        error_msg = f"❌ Error adding images: {str(e)}\n"
        error_msg += "💡 Try again or generate PPT without images."
        return markdown_text, error_msg


def generate_ppt_from_markdown(markdown_text):
    """Generate PowerPoint presentation from markdown text"""
    if not markdown_text or not markdown_text.strip():
        return None, "⚠️ Please create some content first by chatting with the AI."

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

            success_msg = f"✅ PowerPoint generated successfully!\n\n📁 File: {output_filename}\n💾 Location: output/"

            return abs_output_path, success_msg
        finally:
            # Restore original directory
            os.chdir(original_dir)

    except Exception as e:
        LOG.error(f"Error generating PowerPoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, f"❌ Error generating PowerPoint: {str(e)}"


def process_chat_message(user_input, chat_history, session_id, current_markdown):
    """Process a chat message to refine the markdown content with reflection"""
    if not user_input or not user_input.strip():
        return chat_history, current_markdown, ""

    # Chat with bot to refine content using reflection
    updated_history, response, feedback = chat_with_bot(user_input, chat_history, session_id)

    # Update markdown output with the latest response
    return updated_history, response, feedback


def process_enhance_images(markdown_text, session_id):
    """Enhance markdown with AI-selected images"""
    enhanced_markdown, status = enhance_markdown_with_images(markdown_text, session_id)
    return enhanced_markdown, status


def process_generate_ppt(current_markdown):
    """Generate PowerPoint from the current markdown content"""
    ppt_file, status_message = generate_ppt_from_markdown(current_markdown)
    return ppt_file, status_message


def create_gradio_interface():
    """Create the Gradio chatbot interface"""

    with gr.Blocks(title="ChatPPT - AI PowerPoint Generator") as demo:
        # Session state for maintaining user session
        session_id = gr.State(lambda: str(uuid.uuid4()))

        gr.Markdown(
            """
            # 🎨 ChatPPT - AI PowerPoint Generator
            
            Transform your ideas into professional PowerPoint presentations using AI!
            
            **How it works:**
            1. **Chat** with the AI to create and refine your presentation content
            2. **Review** the generated markdown in real-time
            3. **Generate** PowerPoint with optional AI-selected images
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
                    label="Enter your message",
                    placeholder="Chat with the AI to create your presentation...\n\nExample:\n- 我想做一个关于人工智能的演讲\n- 请添加AI的应用领域章节\n- 修改第二章的标题",
                    lines=8
                )

                with gr.Row():
                    send_btn = gr.Button("💬 Send Message", variant="primary")
                    clear_btn = gr.Button("🗑️ Clear All", variant="secondary")

            with gr.Column(scale=1):
                gr.Markdown("### 💬 Chat History")
                chatbot = gr.Chatbot(
                    label="Conversation with AI",
                    height=400
                )

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📄 Current Markdown Content")
                markdown_output = gr.Textbox(
                    label="This is your presentation content that will be converted to PPT",
                    lines=12,
                    interactive=True,
                    placeholder="Your markdown content will appear here as you chat..."
                )

                # Image enhancement and PowerPoint generation
                gr.Markdown("### 🎨 Enhance & Generate")
                with gr.Row():
                    enhance_images_btn = gr.Button(
                        "🖼️ Enhance with AI Images",
                        variant="secondary",
                        size="lg",
                        scale=1
                    )
                    generate_ppt_btn = gr.Button(
                        "📊 Generate PowerPoint",
                        variant="primary",
                        size="lg",
                        scale=1
                    )

                gr.Markdown(
                    """
                    💡 **Workflow**: 
                    1. Chat to create content → 2. (Optional) Enhance with images → 3. Generate PPT
                    """
                )

            with gr.Column():
                gr.Markdown("### 📊 Status & Output")

                # Reflection feedback display
                gr.Markdown("#### 🔄 AI Reflection Feedback")
                feedback_output = gr.Markdown(
                    value="",
                    label="Reflection Process"
                )

                status_output = gr.Textbox(
                    label="Status Messages",
                    lines=6,
                    interactive=False,
                    placeholder="Status messages will appear here..."
                )
                ppt_output = gr.File(
                    label="Download PowerPoint",
                    type="filepath"
                )

        # Event handlers
        def clear_all():
            """Clear all fields and create new session"""
            new_session_id = str(uuid.uuid4())
            return [], "", "", None, "", "", None, new_session_id

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

        # Chat message handler
        send_btn.click(
            fn=process_chat_message,
            inputs=[user_input, chatbot, session_id, markdown_output],
            outputs=[chatbot, markdown_output, feedback_output]
        ).then(
            fn=lambda: "",  # Clear input after sending
            outputs=[user_input]
        )

        # Also allow Enter key to send
        user_input.submit(
            fn=process_chat_message,
            inputs=[user_input, chatbot, session_id, markdown_output],
            outputs=[chatbot, markdown_output, feedback_output]
        ).then(
            fn=lambda: "",
            outputs=[user_input]
        )

        # Image enhancement handler
        enhance_images_btn.click(
            fn=process_enhance_images,
            inputs=[markdown_output, session_id],
            outputs=[markdown_output, status_output]
        )

        # PowerPoint generation handler
        generate_ppt_btn.click(
            fn=process_generate_ppt,
            inputs=[markdown_output],
            outputs=[ppt_output, status_output]
        )

        # Clear all handler
        clear_btn.click(
            fn=clear_all,
            outputs=[chatbot, user_input, markdown_output, ppt_output, status_output, feedback_output, audio_input, session_id]
        )

        gr.Markdown(
            """
            ---
            ### 📌 Tips:
            - 💬 **Chat Mode**: Have a conversation with AI to iteratively build your presentation
            - 🔄 **Reflection Mechanism**: AI automatically reflects on its output up to 3 times to improve quality
            - 📊 **Feedback Display**: View the AI's self-critique and improvement process in real-time
            - 🎤 **Audio Input**: Upload an audio file or record using your microphone for transcription
            - ✍️ **Text Input**: Write in natural language (Chinese or English) to describe your content
            - 🔄 **Iterate**: Keep chatting to refine, add, or modify slides until satisfied
            - ✏️ **Edit Markdown**: You can manually edit the markdown content before generating PPT
            - 🖼️ **Add Images**: Click "Enhance with AI Images" to search and insert relevant images
            - 📊 **Generate**: Click "Generate PowerPoint" when your content is ready
            - 💾 **Storage**: Check the `output/` folder for PPT files and `images/` for downloaded images
            
            ### 🎯 Example Workflow:
            1. **Chat**: "我想做一个关于人工智能的演讲" → AI creates initial structure with reflection
            2. **Observe**: Check the reflection feedback to see how AI improved the content
            3. **Refine**: "请添加AI在医疗领域的应用" → AI adds a new section with reflection
            4. **Review**: Check the markdown content, edit if needed
            5. **Enhance**: Click "🖼️ Enhance with AI Images" → AI finds and adds images to markdown
            6. **Generate**: Click "📊 Generate PowerPoint" → Get your final vivid PPT!
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

