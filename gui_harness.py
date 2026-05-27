#!/usr/bin/env python3
"""
MarkItDown GUI Harness
A simple GUI for converting files to Markdown using the markitdown library.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import traceback
from markitdown import MarkItDown


class MarkItDownGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MarkItDown - File to Markdown Converter")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.md_converter = MarkItDown()
        self.current_file = None
        self.current_markdown = None
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the user interface."""
        # Top frame for file selection
        top_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        top_frame.pack(fill=tk.X)
        
        tk.Label(top_frame, text="Select a file to convert:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        file_frame = tk.Frame(top_frame, bg="#f0f0f0")
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_label = tk.Label(file_frame, text="No file selected", bg="white", fg="#666", font=("Arial", 9), 
                                   relief=tk.SUNKEN, anchor=tk.W, padx=5, pady=5)
        self.file_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Button(file_frame, text="Browse...", command=self._browse_file, bg="#4CAF50", fg="white", 
                 font=("Arial", 10, "bold"), padx=15, pady=5).pack(side=tk.LEFT)
        
        # Control buttons frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=5)
        button_frame.pack(fill=tk.X)
        
        self.convert_btn = tk.Button(button_frame, text="Convert to Markdown", command=self._convert_file,
                                    bg="#2196F3", fg="white", font=("Arial", 11, "bold"), padx=20, pady=8,
                                    state=tk.DISABLED)
        self.convert_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = tk.Button(button_frame, text="Save Markdown", command=self._save_markdown,
                                 bg="#FF9800", fg="white", font=("Arial", 11, "bold"), padx=20, pady=8,
                                 state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Clear", command=self._clear_all,
                 bg="#f44336", fg="white", font=("Arial", 11, "bold"), padx=20, pady=8).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready", bg="#e8f5e9", fg="#2e7d32", font=("Arial", 9),
                                    relief=tk.SUNKEN, anchor=tk.W, padx=5)
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Output text area with label
        output_label_frame = tk.Frame(self.root, padx=10)
        output_label_frame.pack(fill=tk.X, pady=(10, 0))
        tk.Label(output_label_frame, text="Markdown Output:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        # Text area
        text_frame = tk.Frame(self.root, padx=10, pady=5)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Courier", 9),
                                                     bg="white", fg="#333", relief=tk.SUNKEN, borderwidth=1)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Footer
        footer = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=5)
        footer.pack(fill=tk.X)
        tk.Label(footer, text="MarkItDown - Supports PDF, Word, PowerPoint, Excel, Images, Audio, HTML, and more!",
                bg="#f0f0f0", font=("Arial", 8), fg="#999").pack(anchor=tk.W)
    
    def _browse_file(self):
        """Open file browser dialog."""
        file_types = [
            ("All Files", "*.*"),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx *.doc"),
            ("PowerPoint", "*.pptx *.ppt"),
            ("Excel", "*.xlsx *.xls"),
            ("Images", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("HTML", "*.html *.htm"),
            ("Text Files", "*.txt"),
            ("CSV Files", "*.csv"),
            ("JSON Files", "*.json"),
            ("ZIP Files", "*.zip"),
        ]
        
        file_path = filedialog.askopenfilename(title="Select a file to convert", filetypes=file_types)
        
        if file_path:
            self.current_file = Path(file_path)
            self.file_label.config(text=str(self.current_file), fg="#333")
            self.convert_btn.config(state=tk.NORMAL)
            self._update_status(f"Selected: {self.current_file.name}")
            self.output_text.delete(1.0, tk.END)
            self.current_markdown = None
            self.save_btn.config(state=tk.DISABLED)
    
    def _convert_file(self):
        """Convert the selected file to markdown."""
        if not self.current_file:
            messagebox.showwarning("No File", "Please select a file first.")
            return
        
        self.convert_btn.config(state=tk.DISABLED)
        self.output_text.delete(1.0, tk.END)
        self._update_status("Converting...", "#fff3cd")
        
        # Run conversion in a separate thread to prevent UI freezing
        thread = threading.Thread(target=self._convert_file_thread)
        thread.daemon = True
        thread.start()
    
    def _convert_file_thread(self):
        """Convert file in background thread."""
        try:
            self._update_status("Converting...", "#fff3cd")
            
            # Convert the file
            result = self.md_converter.convert(str(self.current_file))
            self.current_markdown = result.text_content
            
            # Update UI
            self.root.after(0, lambda: self.output_text.insert(1.0, self.current_markdown))
            self.root.after(0, lambda: self._update_status(
                f"Successfully converted: {self.current_file.name}", "#e8f5e9"))
            self.root.after(0, lambda: self.convert_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.save_btn.config(state=tk.NORMAL))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}\n\n{traceback.format_exc()}"
            self.root.after(0, lambda: self.output_text.insert(1.0, error_msg))
            self.root.after(0, lambda: self._update_status(
                f"Error converting file: {str(e)}", "#ffebee"))
            self.root.after(0, lambda: self.convert_btn.config(state=tk.NORMAL))
    
    def _save_markdown(self):
        """Save the markdown output to a file."""
        if not self.current_markdown:
            messagebox.showwarning("No Content", "Please convert a file first.")
            return
        
        # Suggest a default filename
        default_name = self.current_file.stem + ".md" if self.current_file else "output.md"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            initialfile=default_name,
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                Path(file_path).write_text(self.current_markdown, encoding="utf-8")
                self._update_status(f"Saved to: {file_path}", "#e8f5e9")
                messagebox.showinfo("Success", f"Markdown saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
                self._update_status(f"Error saving file: {str(e)}", "#ffebee")
    
    def _clear_all(self):
        """Clear all fields and reset the application."""
        self.current_file = None
        self.current_markdown = None
        self.file_label.config(text="No file selected", fg="#666")
        self.output_text.delete(1.0, tk.END)
        self.convert_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self._update_status("Ready")
    
    def _update_status(self, message, bg_color="#e8f5e9"):
        """Update the status label."""
        self.status_label.config(text=message, bg=bg_color)


def main():
    """Main entry point for the GUI."""
    root = tk.Tk()
    app = MarkItDownGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
