# ChatPPT Gradio Application

## Quick Start

### Option 1: Using the Batch File (Windows)
Simply double-click `run_gradio.bat` to start the application.

### Option 2: Manual Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
cd src
python gradio_app.py
```

## Features

1. **Natural Language Input**: Enter your presentation content in natural language (Chinese or English)
2. **AI Transformation**: Azure OpenAI transforms your input into structured markdown format
3. **Automatic PPT Generation**: PowerPoint is automatically generated from the markdown

## How It Works

1. Enter your content in the text box
2. Click "Generate PowerPoint"
3. The AI will:
   - Transform your input to markdown format
   - Parse the markdown into slides
   - Generate a PowerPoint presentation
4. Download your generated PowerPoint file

## Configuration

Make sure your `.env` file contains the required Azure OpenAI credentials:
```
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
AZURE_MODEL=gpt-4.1
AZURE_API_VERSION=2024-12-01-preview
```

## Example Input

```
我想做一个关于人工智能的演讲
包括AI的定义
AI的应用领域
- 医疗健康
- 金融服务
- 自动驾驶
AI的未来发展趋势
```

## Output Location

Generated PowerPoint files are saved in the `output/` directory with timestamps.

## Troubleshooting

### Gradio Not Installed
```bash
pip install gradio
```

### LangChain Not Available
```bash
pip install langchain-openai langchain-core
```

### Azure OpenAI Connection Issues
- Verify your `.env` file credentials
- Check network connectivity
- Ensure the Azure OpenAI endpoint is accessible

