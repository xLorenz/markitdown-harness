#!/usr/bin/env python3
"""
MarkItDown GUI Harness
A beautiful GUI for converting files to Markdown using the markitdown library.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from pathlib import Path
import threading
import traceback
from markitdown import MarkItDown


class ModernButton(tk.Button):
    """Custom modern button with better styling."""
    def __init__(self, parent, **kwargs):
        bg_color = kwargs.pop('bg_color', '#2196F3')
        super().__init__(parent, **kwargs)
        self.config(
            bg=bg_color,
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            padx=12,
            pady=8,
            cursor='hand2',
            activebackground=self._darken(bg_color),
            activeforeground='white',
            highlightthickness=0
        )
    
    @staticmethod
    def _darken(color):
        """Darken a hex color for hover effect."""
        return color


class MarkItDownGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MarkItDown - Elegant File Converter")
        self.root.geometry("1200x850")
        self.root.resizable(True, True)
        
        # Color scheme - modern dark theme with blue accents
        self.colors = {
            'bg_primary': '#0f172a',      # Deep blue-black
            'bg_secondary': '#1e293b',    # Darker slate
            'bg_tertiary': '#334155',     # Slate
            'accent_primary': '#3b82f6',  # Bright blue
            'accent_secondary': '#10b981',# Green (success)
            'accent_warning': '#f59e0b',  # Amber (warning)
            'accent_danger': '#ef4444',   # Red (danger)
            'text_primary': '#f1f5f9',    # Light text
            'text_secondary': '#cbd5e1',  # Muted text
            'border': '#475569',          # Border color
        }
        
        self.root.config(bg=self.colors['bg_primary'])
        
        self.md_converter = MarkItDown()
        self.current_file = None
        self.current_markdown = None
        
        # Queue management
        self.file_queue = []
        self.is_converting = False
        self.output_directory = None
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the user interface."""
        # Header
        self._create_header()
        
        # Main container with two columns
        main_container = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=3,
                                       bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # LEFT PANEL - Queue Management
        left_panel = tk.Frame(main_container, bg=self.colors['bg_secondary'])
        main_container.add(left_panel, width=380)
        
        # Output directory section
        self._create_directory_section(left_panel)
        
        # Queue section
        self._create_queue_section(left_panel)
        
        # RIGHT PANEL - Preview
        right_panel = tk.Frame(main_container, bg=self.colors['bg_secondary'])
        main_container.add(right_panel, width=820)
        
        # Status and preview
        self._create_preview_section(right_panel)
    
    def _create_header(self):
        """Create a beautiful header."""
        header = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Add gradient-like effect with accent line
        accent_line = tk.Frame(header, bg=self.colors['accent_primary'], height=4)
        accent_line.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Title and subtitle
        title_frame = tk.Frame(header, bg=self.colors['bg_secondary'])
        title_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
        title = tk.Label(title_frame, text="📄 MarkItDown", font=('Segoe UI', 28, 'bold'),
                        fg=self.colors['text_primary'], bg=self.colors['bg_secondary'])
        title.pack(anchor=tk.W)
        
        subtitle = tk.Label(title_frame, text="Convert any document to beautiful Markdown", 
                           font=('Segoe UI', 10), fg=self.colors['text_secondary'],
                           bg=self.colors['bg_secondary'])
        subtitle.pack(anchor=tk.W, pady=(2, 0))
    
    def _create_directory_section(self, parent):
        """Create output directory selection."""
        dir_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'], highlightthickness=1,
                            highlightbackground=self.colors['border'])
        dir_frame.pack(fill=tk.X, padx=15, pady=(15, 10), ipady=12)
        
        label = tk.Label(dir_frame, text="📁 Output Directory", font=('Segoe UI', 11, 'bold'),
                        fg=self.colors['text_primary'], bg=self.colors['bg_tertiary'])
        label.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        self.dir_label = tk.Label(dir_frame, text="No directory selected", 
                                 bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'],
                                 font=('Segoe UI', 9), relief=tk.FLAT, anchor=tk.W, padx=8, pady=6,
                                 wraplength=300)
        self.dir_label.pack(fill=tk.X, padx=10, pady=(0, 8))
        
        dir_btn_frame = tk.Frame(dir_frame, bg=self.colors['bg_tertiary'])
        dir_btn_frame.pack(fill=tk.X, padx=10)
        
        btn_select = ModernButton(dir_btn_frame, text="📂 Select Directory", 
                                 command=self._select_output_directory, bg_color=self.colors['accent_primary'])
        btn_select.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        btn_clear = ModernButton(dir_btn_frame, text="✕", 
                                command=self._clear_output_directory, bg_color=self.colors['accent_danger'],
                                width=3)
        btn_clear.pack(side=tk.LEFT)
    
    def _create_queue_section(self, parent):
        """Create queue management."""
        queue_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'], highlightthickness=1,
                              highlightbackground=self.colors['border'])
        queue_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15), ipady=12)
        
        label = tk.Label(queue_frame, text="📋 File Queue", font=('Segoe UI', 11, 'bold'),
                        fg=self.colors['text_primary'], bg=self.colors['bg_tertiary'])
        label.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Queue listbox
        listbox_frame = tk.Frame(queue_frame, bg=self.colors['bg_tertiary'])
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        scrollbar = tk.Scrollbar(listbox_frame, bg=self.colors['bg_secondary'],
                               troughcolor=self.colors['bg_tertiary'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.queue_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set,
                                       font=('Segoe UI', 9), relief=tk.FLAT, borderwidth=0,
                                       bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                       selectmode=tk.SINGLE, highlightthickness=0,
                                       activestyle='none')
        self.queue_listbox.pack(fill=tk.BOTH, expand=True)
        self.queue_listbox.bind('<<ListboxSelect>>', self._on_queue_select)
        scrollbar.config(command=self.queue_listbox.yview)
        
        # Queue count
        self.queue_count_label = tk.Label(queue_frame, text="Queue: 0 files", 
                                         font=('Segoe UI', 9), fg=self.colors['text_secondary'],
                                         bg=self.colors['bg_tertiary'])
        self.queue_count_label.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Queue buttons
        btn_frame = tk.Frame(queue_frame, bg=self.colors['bg_tertiary'])
        btn_frame.pack(fill=tk.X, padx=10)
        
        tk.Button(btn_frame, text="➕ Add Files", command=self._add_files_to_queue,
                 bg=self.colors['accent_primary'], fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, padx=10, pady=6, cursor='hand2', highlightthickness=0).pack(fill=tk.X, pady=3)
        
        tk.Button(btn_frame, text="➖ Remove Selected", command=self._remove_from_queue,
                 bg=self.colors['accent_warning'], fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, padx=10, pady=6, cursor='hand2', highlightthickness=0).pack(fill=tk.X, pady=3)
        
        tk.Button(btn_frame, text="🗑️ Clear Queue", command=self._clear_queue,
                 bg=self.colors['accent_danger'], fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, padx=10, pady=6, cursor='hand2', highlightthickness=0).pack(fill=tk.X, pady=3)
        
        # Separator
        sep = tk.Frame(queue_frame, bg=self.colors['border'], height=1)
        sep.pack(fill=tk.X, padx=10, pady=10)
        
        # Conversion buttons
        self.convert_batch_btn = tk.Button(queue_frame, text="▶️ Convert All Files",
                                          command=self._convert_batch,
                                          bg=self.colors['accent_secondary'], fg='white',
                                          font=('Segoe UI', 11, 'bold'), relief=tk.FLAT,
                                          padx=15, pady=12, cursor='hand2', highlightthickness=0)
        self.convert_batch_btn.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        self.stop_btn = tk.Button(queue_frame, text="⏹️ Stop Conversion",
                                 command=self._stop_conversion,
                                 bg=self.colors['accent_danger'], fg='white',
                                 font=('Segoe UI', 9, 'bold'), relief=tk.FLAT,
                                 padx=10, pady=8, state=tk.DISABLED, cursor='hand2',
                                 highlightthickness=0)
        self.stop_btn.pack(fill=tk.X, padx=10)
    
    def _create_preview_section(self, parent):
        """Create preview and status section."""
        # Status bar
        status_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'], highlightthickness=1,
                               highlightbackground=self.colors['border'])
        status_frame.pack(fill=tk.X, padx=15, pady=(15, 10), ipady=10)
        
        self.status_label = tk.Label(status_frame, text="✓ Ready to convert",
                                    bg=self.colors['bg_secondary'], fg=self.colors['accent_secondary'],
                                    font=('Segoe UI', 9), relief=tk.FLAT, anchor=tk.W, padx=8)
        self.status_label.pack(fill=tk.X, padx=8, pady=(0, 5))
        
        # Progress bar
        progress_style = ttk.Style()
        progress_style.theme_use('clam')
        progress_style.configure('TProgressbar', background=self.colors['accent_secondary'],
                               troughcolor=self.colors['bg_secondary'], bordercolor=self.colors['border'],
                               lightcolor=self.colors['accent_secondary'], darkcolor=self.colors['accent_secondary'])
        
        self.progress_bar = ttk.Progressbar(status_frame, length=400, mode='determinate',
                                           style='TProgressbar', value=0)
        self.progress_bar.pack(fill=tk.X, padx=8, pady=(0, 5))
        
        self.progress_label = tk.Label(status_frame, text="", font=('Segoe UI', 8),
                                      fg=self.colors['text_secondary'], bg=self.colors['bg_tertiary'])
        self.progress_label.pack(anchor=tk.W, padx=8)
        
        # Preview section
        preview_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'], highlightthickness=1,
                                highlightbackground=self.colors['border'])
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15), ipady=12)
        
        label = tk.Label(preview_frame, text="👁️ Preview", font=('Segoe UI', 11, 'bold'),
                        fg=self.colors['text_primary'], bg=self.colors['bg_tertiary'])
        label.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Output text area
        text_frame = tk.Frame(preview_frame, bg=self.colors['bg_tertiary'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        scrollbar = tk.Scrollbar(text_frame, bg=self.colors['bg_secondary'],
                               troughcolor=self.colors['bg_tertiary'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.output_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD,
                                                    font=('Consolas', 9), relief=tk.FLAT,
                                                    bg=self.colors['bg_secondary'],
                                                    fg=self.colors['text_primary'],
                                                    insertbackground=self.colors['accent_primary'],
                                                    highlightthickness=0, borderwidth=0)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output_text.yview)
        
        # Footer hint
        footer = tk.Label(parent, text="💡 Select files to queue → Set output directory → Click 'Convert All Files'",
                         font=('Segoe UI', 8), fg=self.colors['text_secondary'],
                         bg=self.colors['bg_secondary'], relief=tk.FLAT, anchor=tk.W, padx=15, pady=8)
        footer.pack(fill=tk.X)
    
    def _select_output_directory(self):
        """Select the directory where all converted files will be saved."""
        directory = filedialog.askdirectory(title="Select Output Directory for Markdown Files")
        if directory:
            self.output_directory = Path(directory)
            display_text = str(self.output_directory).replace('\\', '/')
            if len(display_text) > 40:
                display_text = "..." + display_text[-37:]
            self.dir_label.config(text=display_text, fg=self.colors['text_primary'])
            self._update_status(f"✓ Output: {self.output_directory.name}", self.colors['accent_secondary'])
    
    def _clear_output_directory(self):
        """Clear the selected output directory."""
        self.output_directory = None
        self.dir_label.config(text="No directory selected", fg=self.colors['text_secondary'])
        self._update_status("Output directory cleared")
    
    def _add_files_to_queue(self):
        """Add multiple files to the conversion queue."""
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
        
        files = filedialog.askopenfilenames(title="Select files to convert", filetypes=file_types)
        
        if files:
            for file_path in files:
                self.file_queue.append(Path(file_path))
            
            self._update_queue_display()
            self._update_status(f"✓ Added {len(files)} file(s) to queue", self.colors['accent_secondary'])
    
    def _update_queue_display(self):
        """Update the queue listbox display."""
        self.queue_listbox.delete(0, tk.END)
        for i, file_path in enumerate(self.file_queue, 1):
            self.queue_listbox.insert(tk.END, f"{i}. {file_path.name}")
        
        self.queue_count_label.config(text=f"Queue: {len(self.file_queue)} file{'s' if len(self.file_queue) != 1 else ''}")
    
    def _on_queue_select(self, event):
        """Handle queue item selection to show preview."""
        selection = self.queue_listbox.curselection()
        if selection:
            idx = selection[0]
            self.current_file = self.file_queue[idx]
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, f"📄 Selected: {self.current_file.name}\n\n" +
                                   "Click '▶️ Convert All Files' to start processing the queue.")
    
    def _remove_from_queue(self):
        """Remove selected file from queue."""
        selection = self.queue_listbox.curselection()
        if selection:
            idx = selection[0]
            removed = self.file_queue.pop(idx)
            self._update_queue_display()
            self._update_status(f"✗ Removed: {removed.name}", self.colors['accent_warning'])
        else:
            messagebox.showwarning("No Selection", "Please select a file to remove from the queue.")
    
    def _clear_queue(self):
        """Clear all files from the queue."""
        if self.file_queue:
            if messagebox.askyesno("Clear Queue", "Remove all files from the queue?"):
                self.file_queue.clear()
                self._update_queue_display()
                self.output_text.delete(1.0, tk.END)
                self._update_status("Queue cleared")
    
    def _convert_batch(self):
        """Convert all files in the queue."""
        if not self.file_queue:
            messagebox.showwarning("Empty Queue", "Please add files to the queue first.")
            return
        
        if not self.output_directory:
            messagebox.showwarning("No Output Directory", "Please select an output directory first.")
            return
        
        # Disable buttons during conversion
        self.convert_batch_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.is_converting = True
        self.progress_bar['value'] = 0
        
        # Run conversion in separate thread
        thread = threading.Thread(target=self._batch_convert_thread)
        thread.daemon = True
        thread.start()
    
    def _batch_convert_thread(self):
        """Convert all files in batch."""
        total = len(self.file_queue)
        successful = 0
        failed = 0
        failed_files = []
        
        for idx, file_path in enumerate(self.file_queue):
            if not self.is_converting:
                break
            
            try:
                # Update progress
                progress = int((idx / total) * 100)
                self.root.after(0, self.progress_bar.__setitem__, 'value', progress)
                
                progress_text = f"Converting {idx + 1}/{total}: {file_path.name}"
                self.root.after(0, self._update_progress, progress_text)
                
                status_text = f"⏳ Converting ({idx + 1}/{total}): {file_path.name}"
                def update_status_during_conversion(text=status_text):
                    self._update_status(text, self.colors['accent_warning'])
                self.root.after(0, update_status_during_conversion)
                
                # Convert file
                result = self.md_converter.convert(str(file_path))
                
                # Determine output filename
                output_filename = file_path.stem + ".md"
                output_path = self.output_directory / output_filename
                
                # Handle duplicate filenames
                counter = 1
                while output_path.exists():
                    output_path = self.output_directory / f"{file_path.stem}_{counter}.md"
                    counter += 1
                
                # Save file
                output_path.write_text(result.text_content, encoding="utf-8")
                
                # Update display with current file preview (preview only first 2000 chars)
                preview_text = result.text_content[:2000]
                if len(result.text_content) > 2000:
                    preview_text += f"\n\n... (showing 2000 of {len(result.text_content)} characters)"
                
                def update_preview(text=preview_text):
                    self.output_text.delete(1.0, tk.END)
                    self.output_text.insert(1.0, text)
                
                self.root.after(0, update_preview)
                
                successful += 1
                
            except Exception as e:
                failed += 1
                failed_files.append((file_path.name, str(e)))
                error_msg = f"✗ Error: {file_path.name}"
                def show_error(msg=error_msg):
                    self._update_status(msg, self.colors['accent_danger'])
                self.root.after(0, show_error)
        
        # Completion
        if self.is_converting:
            self.root.after(0, self.progress_bar.__setitem__, 'value', 100)
            summary = f"✓ Batch complete! {successful} converted"
            if failed > 0:
                summary += f", {failed} failed"
            
            self.root.after(0, self._update_progress, summary)
            
            def show_completion():
                self._update_status(summary, self.colors['accent_secondary'])
                messagebox.showinfo("✓ Conversion Complete", 
                    f"Successfully converted: {successful}/{total} files\n\nSaved to:\n{self.output_directory}")
            
            self.root.after(0, show_completion)
        else:
            def show_stopped():
                self._update_status("⏹️ Conversion stopped", self.colors['accent_warning'])
            self.root.after(0, show_stopped)
        
        # Re-enable buttons
        def enable_buttons():
            self.convert_batch_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.progress_bar['value'] = 0
        
        self.root.after(0, enable_buttons)
        self.is_converting = False
    
    def _stop_conversion(self):
        """Stop the ongoing batch conversion."""
        self.is_converting = False
        self._update_status("Stopping conversion...", self.colors['accent_warning'])
    
    def _update_progress(self, message):
        """Update the progress label."""
        self.progress_label.config(text=message)
    
    def _update_status(self, message, bg_color=None):
        """Update the status label."""
        if bg_color is None:
            bg_color = self.colors['bg_secondary']
        self.status_label.config(text=message, bg=bg_color)
    
    def _save_markdown(self):
        """Save the current markdown output to a file."""
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
                self._update_status(f"✓ Saved: {Path(file_path).name}", self.colors['accent_secondary'])
                messagebox.showinfo("✓ Success", f"Markdown saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("✗ Error", f"Failed to save file:\n{str(e)}")
                self._update_status(f"✗ Error saving file", self.colors['accent_danger'])


def main():
    """Main entry point for the GUI."""
    root = tk.Tk()
    app = MarkItDownGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
