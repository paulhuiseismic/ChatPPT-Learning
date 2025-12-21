# 🚀 Quick Start Guide - Enhanced ChatPPT

## Start the Application

```bash
# Option 1: Batch file (Windows)
run_gradio.bat

# Option 2: Command line
python src\gradio_app.py

# Option 3: Test first, then run
python test_enhanced_gradio.py
python src\gradio_app.py
```

## Using the Chat Interface

### Step 1: Start a Conversation

Type your presentation idea in the text input box:

```
Examples:
- "我想做一个关于人工智能的演讲，包括AI的定义、应用和未来发展"
- "Create a presentation about renewable energy"
- "帮我准备一个产品发布会的PPT"
```

Click **"💬 Send Message"** or press **Enter**

### Step 2: Refine Your Content

Continue chatting to improve the presentation:

```
Examples:
- "请添加一个关于机器学习的章节"
- "Add more details about solar energy"
- "修改第二页的标题为'技术架构'"
- "Remove the last slide"
- "Make slide 3 more detailed"
```

### Step 3: Review Markdown

Check the **"Current Markdown Content"** box to see your presentation structure.

You can also **manually edit** the markdown if needed!

### Step 4: Enhance with Images (Optional but Recommended)

1. Click **"🖼️ Enhance with AI Images"** button
2. Wait for processing (10-30 seconds)
3. Check status message:
   - ✅ Shows how many images were added
   - 📁 Shows where images are saved
   - 🎨 Confirms markdown was updated

The markdown will now contain image references like:
```markdown
## Slide Title
- Content here

![Slide Title](images/session_xxx/Slide_Title_1.jpeg)
```

### Step 5: Generate PowerPoint

1. Click **"📊 Generate PowerPoint"**

2. Wait for processing (3-5 seconds)

3. **Download** your PowerPoint file!

**Note**: If you enhanced with images in Step 4, your PPT will include them!

## Features Overview

### 💬 Chat with AI
- Natural language conversation
- Maintains full history
- Iterative refinement
- Context-aware responses

### 🖼️ Smart Images (Two-Step Process)
1. **Enhance Button**: Click to start image search
   - AI analyzes each slide
   - Searches Bing for relevant images
   - Selects high-resolution images
   - Downloads to `images/` folder
   - Inserts image references into markdown
   - Shows clear status and image count
2. **Generate Button**: Creates PPT with images included

### 🎤 Audio Input (Optional)
1. Click microphone icon or upload audio file
2. Click **"🎵 Transcribe Audio"**
3. Text appears in input box
4. Continue chatting normally

### 📝 Live Preview
- See markdown update in real-time
- Edit manually if needed
- See image references after enhancement
- Copy/save for later use

## Tips & Tricks

### 🎯 Get Better Results

**Be Specific**: "Add a slide about AI applications in healthcare"
Rather than: "Add more content"

**Iterate**: Don't try to get everything perfect in one message
- First message: Create basic structure
- Follow-up messages: Refine details

**Use Examples**: "Make it like a TED talk style presentation"

### 🖼️ Image Settings

**When to Enable Images:**
- ✅ Public presentations
- ✅ Marketing materials
- ✅ Educational content
- ✅ Conference talks

**When to Disable Images:**
- ☐ Internal reports
- ☐ Data-heavy presentations
- ☐ Quick drafts
- ☐ When you'll add images manually

### 💡 Common Workflows

**Workflow 1: Quick Draft (No Images)**
```
1. Chat: "Create presentation about [topic]"
2. Review markdown
3. Click "📊 Generate PowerPoint" (skip image enhancement)
4. Done! Fast text-only PPT
```

**Workflow 2: Full Production (With Images)**
```
1. Chat: "Create presentation about [topic]"
2. Refine: "Add section about [detail]"
3. Review markdown
4. Click "🖼️ Enhance with AI Images" → Wait for images
5. Click "📊 Generate PowerPoint"
6. Download vivid PPT with images!
```

**Workflow 3: Custom Images**
```
1. Chat: Create structure
2. Click "🖼️ Enhance with AI Images"
3. Review image paths in markdown
4. Manually replace some image paths if desired
5. Click "📊 Generate PowerPoint"
6. Get PPT with mix of AI and custom images
```

**Workflow 4: Collaborative**
```
1. Chat: Create structure
2. Copy markdown to share with team
3. Team edits markdown (can add image paths)
4. Paste back into app
5. Click "📊 Generate PowerPoint"
```

## Troubleshooting

### ❌ "No images found"
- **Solution**: Continue anyway, PPT will be text-only
- **Cause**: Network issues or search returned no results
- **Action**: Try disabling images or check internet connection

### ⏱️ "Timeout errors"
- **Solution**: App handles this automatically, skips failed images
- **Cause**: Some image URLs are slow/blocked
- **Action**: No action needed, app continues

### 🔄 "Want to start over"
- **Solution**: Click **"🗑️ Clear All"** button
- **Effect**: New session, fresh start

### 📝 "Markdown looks wrong"
- **Solution**: Edit it directly in the markdown box
- **Or**: Chat with AI: "Fix the formatting"

## Output Location

All generated PowerPoint files are saved to:
```
C:\Workspace\AILearning\AgentLearning\ChatPPT-Learning\output\
```

Filename format: `[Title]_[Timestamp].pptx`

Example: `AI技术介绍_20251221_175430.pptx`

## Advanced Usage

### Custom Prompts

Edit these files to customize AI behavior:
- `prompts/content_formatter.txt` - Controls how AI structures content
- `prompts/image_advisor.txt` - Controls image selection

### Session Management

Each time you click "Clear All", you get a new session.

Sessions are isolated - changes in one don't affect others.

### Manual Markdown Editing

The markdown box is editable! You can:
- Copy existing presentations
- Paste from other sources
- Manually fix formatting
- Combine multiple sources

Then click "Generate PowerPoint" to convert it.

## Markdown Format Guide

### Basic Structure

```markdown
# Presentation Title

## Slide 1 Title
- Bullet point 1
- Bullet point 2
- Bullet point 3

## Slide 2 Title
- More content
- More bullets

![Slide 2 Title](path/to/image.jpg)
```

### What the AI Creates

- `#` = Presentation title (first slide)
- `##` = Slide title
- `-` = Bullet points
- `![...]` = Images (added automatically if enabled)

### You Can Add

- **Bold text**: `**bold**`
- *Italic text*: `*italic*`
- Lists with numbers: `1. Item`
- Sub-bullets: Indent with spaces

## Keyboard Shortcuts

- **Enter**: Send message (in chat input)
- **Ctrl+A**: Select all (in markdown box)
- **Ctrl+C**: Copy markdown
- **Ctrl+V**: Paste into markdown box

## Performance Notes

### Timing Expectations

- **Chat Response**: 2-5 seconds
- **Generate PPT (no images)**: 3-5 seconds
- **Generate PPT (with images)**: 10-30 seconds
  - Depends on number of slides
  - 3 images per slide searched
  - Network speed matters

### Resource Usage

- **Memory**: ~2-4 GB (includes AI models)
- **Disk**: ~100 KB per PPT file
- **Network**: Active during chat and image download

## Support

### Check Logs

Logs are saved to: `logs/app.log`

### Test Installation

```bash
python test_enhanced_gradio.py
```

Should show: ✅ All tests passed!

### Common Issues

1. **Gradio not installed**: `pip install gradio`
2. **LangChain errors**: Check Azure OpenAI config
3. **Image errors**: Images are optional, PPT still works

---

## Example Session

```
User: "Create a presentation about Python programming"

AI: [Generates structure]
# Python Programming

## Introduction to Python
- History and overview
- Why Python is popular
...

User: "Add a slide about data science applications"

AI: [Adds new slide]
## Data Science with Python
- NumPy and Pandas
- Machine learning libraries
...

User: "Perfect! Let's add images"

[User clicks "🖼️ Enhance with AI Images"]

Status: ✅ Successfully added 4 images to your presentation!
        📁 Images saved to: images/session_abc123/
        🎨 Markdown has been updated with image references.

[Markdown now shows:]
## Introduction to Python
- History and overview
- Why Python is popular

![Introduction to Python](images/session_abc123/Introduction_to_Python_1.jpeg)

[User clicks "📊 Generate PowerPoint"]

Status: ✅ PowerPoint generated successfully!
        📁 File: Python_Programming_20251221_180000.pptx
        💾 Location: output/

[User downloads and presents! 🎉]
```

---

**Ready to create amazing presentations? Start chatting! 💬**


