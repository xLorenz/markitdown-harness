# MarkItDown GUI Harness

A simple, easy-to-use graphical interface for the [MarkItDown](https://github.com/microsoft/markitdown) library - a powerful tool for converting PDFs, Word documents, PowerPoint presentations, Excel sheets, images, audio, HTML, and more to Markdown.

## Quick Start

### Windows
Simply **double-click** `run.bat` to start the converter!

### macOS/Linux
Run the following command:
```bash
bash run.sh
```

Or directly:
```bash
python3 gui_harness.py
```

## Features

✅ **Easy File Selection** - Browse and select any supported file type  
✅ **One-Click Conversion** - Convert to Markdown with a single click  
✅ **Live Preview** - View the converted Markdown immediately  
✅ **Save Output** - Save the Markdown to a file  
✅ **Supports Multiple Formats**:
   - 📄 PDF files
   - 📝 Word documents (.docx, .doc)
   - 🎤 PowerPoint presentations (.pptx, .ppt)
   - 📊 Excel spreadsheets (.xlsx, .xls)
   - 🖼️ Images (.png, .jpg, .jpeg, .gif, .bmp) - with OCR support
   - 🎵 Audio files - with transcription support
   - 🌐 HTML files
   - 📋 CSV, JSON, XML files
   - 🗂️ ZIP files
   - 📖 ePub files
   - 🎬 YouTube URLs

## Installation

The Python environment and all dependencies have been automatically installed when you cloned this repository.

If you need to reinstall dependencies manually:

```bash
pip install -e packages/markitdown[all]
```

## Usage

1. **Launch the GUI**
   - Windows: Double-click `run.bat`
   - macOS/Linux: Run `bash run.sh`

2. **Select a File**
   - Click "Browse..." and choose the file you want to convert

3. **Convert**
   - Click "Convert to Markdown" button
   - The conversion will happen in the background

4. **View & Save**
   - The markdown output will appear in the text area
   - Click "Save Markdown" to save the output to a file
   - Or copy the text directly from the preview area

## Supported File Types

- **Documents**: PDF, Word (.docx, .doc), PowerPoint (.pptx, .ppt), Excel (.xlsx, .xls)
- **Images**: PNG, JPG, JPEG, GIF, BMP (with EXIF metadata and OCR)
- **Audio**: MP3, WAV, FLAC, and more (with transcription)
- **Web**: HTML files and YouTube URLs
- **Data**: CSV, JSON, XML, ZIP
- **eBooks**: ePub files
- **Plain Text**: TXT and other text-based formats

## Troubleshooting

### "No module named 'markitdown'"
The Python environment hasn't been set up. Run:
```bash
python -m pip install -e packages/markitdown[all]
```

### Large files taking too long to convert
Some file types (especially PDFs and images with OCR) may take longer to process. The GUI remains responsive during conversion.

### Missing optional features
Some features require additional dependencies (e.g., OCR, audio transcription). These are included in the `[all]` installation. If you're having issues, try:
```bash
python -m pip install -e packages/markitdown[all]
```

## Notes

- The conversion preserves important document structure including headings, lists, tables, and links
- Output is optimized for use with Large Language Models (LLMs) like GPT-4
- For best results with OCR and transcription, ensure you have sufficient system resources available
- Large files (>100MB) may require more time and memory to process

## License

This project is based on [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft, licensed under the MIT License.
