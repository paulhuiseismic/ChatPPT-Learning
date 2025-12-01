# 🚀 ChatPPT Gradio - Quick Start Guide

## What is This?

A web-based AI-powered PowerPoint generator that:
- Takes your ideas in **natural language** (Chinese or English)
- Uses **Azure OpenAI** to structure them into markdown
- Automatically **generates professional PowerPoint** presentations

## Installation (One-Time Setup)

```bash
# Navigate to project directory
cd C:\Workspace\AILearning\AgentLearning\ChatPPT-Learning

# Install all dependencies
pip install -r requirements.txt
```

## Running the Application

### Option 1: Double-click `run_gradio.bat` (Easiest)

### Option 2: Command Line
```bash
cd src
python gradio_app.py
```

### Option 3: PowerShell
```powershell
cd C:\Workspace\AILearning\AgentLearning\ChatPPT-Learning\src
python gradio_app.py
```

## Access the Web Interface

After starting, open your browser to:
```
http://127.0.0.1:7861
```

**Note**: The application will automatically find an available port if 7861 is busy.

## Example Usage

### Step 1: Enter Your Content
Type in the text box (Chinese or English):
```
我想做一个关于云计算的演讲
包括云计算的定义
云计算的优势
- 成本效益
- 灵活性
- 可扩展性
云计算的应用场景
```

### Step 2: Click "Generate PowerPoint"
The system will:
1. Transform your text to structured markdown ✨
2. Parse it into slides 📑
3. Create a PowerPoint presentation 📊

### Step 3: Download Your Presentation
Click the download link and enjoy your professional slides! 🎉

## Troubleshooting

### Can't start the application?
```bash
# Check Python is installed
python --version

# Reinstall dependencies
pip install -r requirements.txt
```

### "TypeError: Chatbot.__init__() got an unexpected keyword argument 'type'"
This error has been **fixed** in the latest version. If you still see it:
```bash
# Update to the latest code
git pull
# Or ensure you have the fixed version of gradio_app.py
```

### Azure OpenAI errors?
Check your `.env` file has:
```env
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
AZURE_MODEL=gpt-4.1
```

### Still having issues?
Check the detailed guide: `docs/GRADIO_SETUP_GUIDE.md`

## Tips

✅ **Write naturally** - The AI understands context  
✅ **Use bullet points** - They become slide bullets  
✅ **Organize logically** - AI will structure into slides  
✅ **Include images** - Format: `![desc](images/file.png)`

## Output Location

All generated presentations are saved in:
```
output/your_presentation_YYYYMMDD_HHMMSS.pptx
```

## Need Help?

1. Check logs: `logs/app.log`
2. Read full guide: `docs/GRADIO_SETUP_GUIDE.md`
3. Review summary: `docs/GRADIO_ENHANCEMENT_SUMMARY.md`

---

**Enjoy creating presentations with AI! 🎨**

