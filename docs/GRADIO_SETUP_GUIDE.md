# ChatPPT Gradio Application - Setup and Usage Guide

## Overview

This enhanced ChatPPT application provides a Gradio-based web interface that:
1. Takes natural language input from users
2. Uses Azure OpenAI to transform it into markdown format
3. Automatically generates PowerPoint presentations from the markdown

## Installation

### Step 1: Install Required Packages

```bash
cd C:\Workspace\AILearning\AgentLearning\ChatPPT-Learning
pip install -r requirements.txt
```

**Note**: The application requires Gradio 6.x (tested with 6.0.1). The code has been updated for compatibility.

Or install packages individually:
```bash
pip install python-pptx gradio openai langchain-openai langchain-core python-dotenv loguru Pillow
```

### Step 2: Verify Installation

Run the test script to verify everything is working:
```bash
python test_gradio_app.py
```

## Running the Application

### Method 1: Using the Batch File (Recommended for Windows)
```bash
# Simply double-click: run_gradio.bat
# Or run from command line:
run_gradio.bat
```

### Method 2: Manual Start
```bash
cd src
python gradio_app.py
```

### Method 3: From PowerShell
```powershell
cd C:\Workspace\AILearning\AgentLearning\ChatPPT-Learning\src
python gradio_app.py
```

## Using the Application

1. **Access the Web Interface**
   - After starting, open your browser to: http://127.0.0.1:7861
   - The Gradio interface will load automatically
   - **Note**: Port may vary if 7861 is busy

2. **Enter Your Content**
   - Type your presentation content in natural language (Chinese or English)
   - Example:
     ```
     我想做一个关于人工智能的演讲
     包括AI的定义
     AI的应用领域
     - 医疗健康
     - 金融服务
     - 自动驾驶
     AI的未来发展趋势
     ```

3. **Generate PowerPoint**
   - Click "🚀 Generate PowerPoint"
   - Watch as the AI:
     - Transforms your input to markdown
     - Parses it into slides
     - Creates the PowerPoint file
   
4. **Download Your Presentation**
   - The generated file will appear in the download section
   - Files are also saved in the `output/` folder with timestamps

## Features

### 1. Natural Language Processing
- Supports both Chinese and English input
- AI understands context and structures content appropriately

### 2. Chat History
- View the conversation between you and the AI
- See the markdown transformation in real-time

### 3. Markdown Preview
- See the generated markdown before PowerPoint creation
- Verify the structure matches your intent

### 4. Automatic File Management
- Files are automatically timestamped
- No risk of overwriting previous presentations
- All files saved in `output/` directory

## Configuration

### Azure OpenAI Settings
Ensure your `.env` file contains:
```env
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com/
AZURE_MODEL=gpt-4.1
AZURE_API_VERSION=2024-12-01-preview
```

### Layout Mapping
Configure in `config.json`:
```json
{
  "input_mode": "text",
  "ppt_template": "templates/MasterTemplate.pptx",
  "layout_mapping": {
    "Title Only": 0,
    "Title and Content": 1,
    "Title and Picture": 2,
    "Title, Content, and Picture": 3
  }
}
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'gradio'"
**Solution:**
```bash
pip install gradio
```

### Issue: "TypeError: Chatbot.__init__() got an unexpected keyword argument 'type'"
**Solution:**
This issue has been **fixed** in the latest version. The code is now compatible with Gradio 6.x.
If you still encounter this error:
```bash
# Ensure you have the latest version
git pull
# Or verify gradio_app.py doesn't have type="messages" in Chatbot initialization
```

### Issue: "LangChain is not installed"
**Solution:**
```bash
pip install langchain-openai langchain-core
```

### Issue: Azure OpenAI Connection Error
**Solution:**
- Check your `.env` file credentials
- Verify network connectivity
- Ensure the Azure OpenAI service is accessible
- Check API key validity

### Issue: Template Not Found
**Solution:**
- Verify `templates/MasterTemplate.pptx` exists
- Check `config.json` for correct template path

### Issue: Image Not Inserted
**Solution:**
- Ensure image paths in markdown are relative to project root
- Example: `![chart](images/performance_chart.png)`
- Verify images exist in the specified location

## File Structure

```
ChatPPT-Learning/
├── src/
│   ├── gradio_app.py          # Main Gradio application
│   ├── main.py                 # Original CLI application
│   ├── input_parser.py         # Markdown parser
│   ├── ppt_generator.py        # PowerPoint generator
│   ├── azure_openai.py         # Azure OpenAI client
│   ├── config.py               # Configuration loader
│   ├── layout_manager.py       # Slide layout manager
│   └── logger.py               # Logging configuration
├── prompts/
│   └── content_formatter.txt   # System prompt for AI
├── templates/
│   └── MasterTemplate.pptx     # PowerPoint template
├── output/                     # Generated presentations
├── images/                     # Image resources
├── config.json                 # App configuration
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── run_gradio.bat             # Windows launcher
└── test_gradio_app.py         # Test script
```

## Advanced Usage

### Using Markdown Directly
If you already have markdown content, you can:
1. Paste it directly into the input box
2. The system will parse and generate the PowerPoint
3. AI transformation can be skipped if the format is correct

### Customizing Templates
1. Modify `templates/MasterTemplate.pptx`
2. Update layout mappings in `config.json`
3. Restart the application

### Adding Images
Include images in your markdown:
```markdown
## Slide with Image
- Content here
![Description](images/your_image.png)
```

## Example Workflows

### Example 1: Business Presentation
**Input:**
```
公司Q1业绩汇报
业绩概述：收入增长20%，利润提升15%
主要成就：新产品发布，市场份额增加
未来计划：扩展海外市场，加强研发投入
```

### Example 2: Technical Presentation
**Input:**
```
Machine Learning Overview
Introduction to ML
- Supervised Learning
- Unsupervised Learning
- Reinforcement Learning
Applications
- Computer Vision
- Natural Language Processing
- Recommendation Systems
```

## Performance Tips

1. **Faster Generation**: Keep presentations to 10-15 slides for optimal performance
2. **Image Optimization**: Use compressed images (< 2MB) for better performance
3. **Batch Processing**: Process multiple presentations in sequence rather than simultaneously

## Support

For issues or questions:
1. Check the logs in `logs/app.log`
2. Review the error messages in the Gradio interface
3. Run `test_gradio_app.py` to diagnose issues

## Comparison: Gradio App vs CLI

| Feature | Gradio App | CLI (main.py) |
|---------|-----------|---------------|
| AI Transformation | ✅ Yes | ❌ No |
| Web Interface | ✅ Yes | ❌ No |
| Chat History | ✅ Yes | ❌ No |
| Direct Markdown Input | ✅ Yes | ✅ Yes |
| Batch Processing | ❌ No | ✅ Yes (via scripts) |
| User-Friendly | ✅ High | ⚠️ Medium |

Both tools are complementary - use the Gradio app for interactive work and the CLI for automation.

