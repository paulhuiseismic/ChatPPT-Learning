# ChatPPT-Learning

AI-powered PowerPoint presentation generator with web interface.

## 🌟 Features

### ✨ NEW: Gradio Web Interface
- **Natural Language Input**: Describe your presentation in plain text
- **AI Transformation**: Azure OpenAI converts your ideas to structured markdown
- **Automatic Generation**: Creates professional PowerPoint presentations
- **User-Friendly**: No coding required, just use the web interface

### Original Features
- **Markdown to PowerPoint**: Convert markdown files to PPTX
- **Template Support**: Use custom PowerPoint templates
- **Layout Management**: Flexible slide layouts
- **Image Support**: Include images in your slides

## 🚀 Quick Start

### Web Interface (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Start the web interface
cd src
python gradio_app.py

# Open browser to: http://127.0.0.1:7861
```

**Note**: Compatible with Gradio 6.x. All compatibility issues have been resolved.

### Command Line
```bash
# Generate PPT from markdown file
python src/main.py inputs/test_input.md
```

## 📖 Documentation

**📚 [Complete Documentation Hub](docs/README.md)** - All documentation organized in one place

### Quick Links
- **[Quick Status](docs/QUICK_STATUS.md)** ⭐ Current working setup and usage
- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 2 minutes
- **[Project Status](PROJECT_STATUS.md)** - Current version and verified features

### Setup & Troubleshooting
- **[PyTorch Installation](docs/PYTORCH_INSTALLATION_TROUBLESHOOTING.md)** - Fix installation issues
- **[GPU Setup (Blackwell)](docs/BLACKWELL_GPU_SETUP.md)** - GPU compatibility guide
- **[Complete Fix Summary](docs/FINAL_FIX_STATUS.md)** - All issues resolved (Dec 19, 2025)

### Feature Guides
- **[Gradio Web Interface](docs/GRADIO_SETUP_GUIDE.md)** - Complete web interface guide
- **[MiniCPM-V Vision Model](docs/QUICK_STATUS.md)** - Image analysis with CPU fallback
- **[PPT Input Format](docs/ppt_input_format.md)** - Markdown format guide

## 💡 Example

**Input (Natural Language):**
```
我想做一个关于人工智能的演讲
包括AI的定义
AI的应用领域
AI的未来发展
```

**Output:** Professional PowerPoint presentation with structured slides

## 🛠️ Requirements

- Python 3.8+
- Gradio 6.x (tested with 6.0.1)
- Azure OpenAI API access (for web interface)
- See `requirements.txt` for package dependencies

**Latest Update**: Fixed Gradio 6.x compatibility issues. Application now runs smoothly with the latest Gradio version.

## 📁 Project Structure

```
ChatPPT-Learning/
├── src/
│   ├── gradio_app.py          # Web interface (NEW)
│   ├── main.py                 # CLI application
│   ├── input_parser.py         # Markdown parser
│   └── ppt_generator.py        # PPT generator
├── templates/                  # PowerPoint templates
├── prompts/                    # AI prompts
├── output/                     # Generated presentations
├── docs/                       # Documentation
└── requirements.txt            # Dependencies
```

## 🔧 Configuration

Create a `.env` file with your Azure OpenAI credentials:
```env
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_MODEL=gpt-4.1
AZURE_API_VERSION=2024-12-01-preview
```

## 📝 License

See [LICENSE](LICENSE) file for details.

