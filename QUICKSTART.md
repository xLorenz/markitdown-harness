# MarkItDown GUI Harness - Setup & Usage Guide

## What You Have

Your MarkItDown setup is complete! You have:

1. **The full MarkItDown repository** - A powerful Python library for converting documents to Markdown
2. **GUI Harness** - A simple graphical interface (`gui_harness.py`) that makes it easy to use
3. **Quick launchers** - Easy ways to start the GUI

## Quick Start

### Windows Users
1. Open the `markitdown` folder in File Explorer
2. **Double-click `run.bat`** - This launches the GUI
3. A window will open with the converter interface
4. Click "Browse..." to select a file
5. Click "Convert to Markdown" to convert it
6. Click "Save Markdown" to save the output

### macOS/Linux Users
```bash
cd ~/Desktop/markitdown
python3 gui_harness.py
```

Or run the launch script:
```bash
bash run.sh
```

## The GUI Harness Features

Once you launch the GUI, you get:

- **File Browser** - Easy file selection with filtering by type
- **Convert Button** - One-click conversion to Markdown
- **Live Preview** - See the Markdown output immediately
- **Save Button** - Save the output to a `.md` file
- **Status Updates** - Real-time conversion status

## Supported File Formats

The converter supports converting these file types to Markdown:

### Documents
- 📄 PDF files
- 📝 Word documents (.docx, .doc)
- 🎤 PowerPoint presentations (.pptx, .ppt)
- 📊 Excel spreadsheets (.xlsx, .xls)

### Media & Images
- 🖼️ Images (.png, .jpg, .jpeg, .gif, .bmp)
  - Extracts EXIF metadata
  - Performs OCR (Optical Character Recognition)
- 🎵 Audio files (.mp3, .wav, .m4a, .flac, etc.)
  - Transcribes audio to text with speech recognition

### Web & Data
- 🌐 HTML files
- 📋 CSV files
- 📊 JSON files
- 🗂️ XML files
- 🗂️ ZIP files (processes all files in archive)
- 🎬 YouTube URLs (extracts transcript)
- 📖 ePub files

### Text Formats
- 📄 Plain text files
- Any other text-based format

## File Structure

```
markitdown/
├── run.bat                    # Windows launcher - DOUBLE-CLICK TO RUN
├── run.sh                     # macOS/Linux launcher
├── gui_harness.py             # The GUI application
├── test_setup.py              # Test script to verify installation
├── GUI_GUIDE.md               # This file
├── QUICKSTART.md              # You're reading this
├── packages/
│   ├── markitdown/            # Main library
│   ├── markitdown-mcp/        # Model Context Protocol server
│   ├── markitdown-ocr/        # OCR plugin
│   └── markitdown-sample-plugin/
├── README.md                  # Original MarkItDown README
└── ... (other repo files)
```

## Installation Status

✅ Repository cloned  
✅ Python environment configured (Python 3.11)  
✅ MarkItDown library installed with all optional features  
✅ GUI harness created  
✅ Launchers created  

## How to Use - Step by Step

### First Time Launch

1. **Navigate to the markitdown folder**
   - Windows: Open File Explorer to `C:\Users\{YourUsername}\Desktop\markitdown`
   - macOS/Linux: Open terminal and navigate to the folder

2. **Launch the GUI**
   - Windows: Double-click `run.bat`
   - macOS/Linux: Run `python3 gui_harness.py`

### Converting Files

1. **Select a File**
   - Click the "Browse..." button
   - Navigate to your file (PDF, Word doc, image, etc.)
   - Click "Open"

2. **Convert**
   - Click "Convert to Markdown"
   - Wait for the conversion to complete (status updates at bottom)
   - View the Markdown output in the text area

3. **Save or Copy**
   - To save: Click "Save Markdown" and choose a location
   - To copy: Select text in the output area and press Ctrl+C

4. **Convert Another File**
   - Click "Browse..." to select a new file
   - Repeat steps 2-3

### Clear & Reset
- Click "Clear" button to reset everything and start over

## Troubleshooting

### "run.bat doesn't work"
- Make sure Python 3.10+ is installed
- Try running `python gui_harness.py` in the terminal instead
- Check that you're in the correct `markitdown` directory

### GUI doesn't appear
- The GUI might be initializing. Wait a moment.
- Try running from terminal to see any error messages:
  ```
  python gui_harness.py
  ```

### Conversion is slow
- Large files (>50MB) or PDFs with many pages may take time
- The GUI remains responsive - no need to force quit
- OCR on images and audio transcription require more processing time

### "Module not found" errors
- Reinstall the package:
  ```
  pip install -e packages/markitdown[all]
  ```

### Python not found
- Make sure Python 3.10+ is installed: https://www.python.org/
- On Windows, add Python to PATH during installation

## Command Line Usage (Advanced)

If you prefer command line, you can use MarkItDown directly:

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("path/to/file.pdf")
print(result.text_content)  # Print the Markdown
```

Or use the CLI:
```bash
python -m markitdown "file.pdf" > output.md
```

## Tips & Tricks

- **OCR on Images**: When converting image files, the tool automatically extracts text using OCR
- **Audio Transcription**: Audio files are transcribed to text automatically
- **Preserve Structure**: The converter preserves headings, lists, tables, and links
- **LLM-Optimized**: Output Markdown is optimized for use with AI language models
- **Large Files**: For very large files, consider splitting them first

## What Gets Converted

The converter is designed to extract:
- Text content
- Document structure (headings, lists, tables)
- Links and URLs
- Metadata (dates, authors, etc. when available)
- Images as references (with alt text)
- Tables in Markdown format

## Next Steps

1. **Try it out!** Select a sample file and see it in action
2. **Integrate**: You can call the Python library from your own scripts
3. **Explore**: Check out `packages/markitdown/` for advanced usage
4. **Customize**: Modify `gui_harness.py` to add your own features

## More Information

- **Official Repository**: https://github.com/microsoft/markitdown
- **PyPI Package**: https://pypi.org/project/markitdown/
- **Built by**: Microsoft's AutoGen Team

---

**Ready to convert?** Just double-click `run.bat` (Windows) or run `python3 gui_harness.py` (macOS/Linux)! 🚀
