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
        self.root.geometry("1100x800")
        self.root.resizable(True, True)
        
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
        # Create main container with two columns
        main_container = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=5)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # LEFT PANEL - Queue Management
        left_panel = tk.Frame(main_container)
        main_container.add(left_panel, width=350)
        
        # Output directory section
        dir_frame = tk.LabelFrame(left_panel, text="Output Directory", font=("Arial", 10, "bold"), padx=10, pady=10)
        dir_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.dir_label = tk.Label(dir_frame, text="Not set", bg="white", fg="#666", font=("Arial", 9),
                                 relief=tk.SUNKEN, anchor=tk.W, padx=5, pady=5)
        self.dir_label.pack(fill=tk.X, padx=(0, 5), pady=(0, 5))
        
        dir_btn_frame = tk.Frame(dir_frame)
        dir_btn_frame.pack(fill=tk.X)
        tk.Button(dir_btn_frame, text="Select Directory", command=self._select_output_directory,
                 bg="#4CAF50", fg="white", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=2)
        tk.Button(dir_btn_frame, text="Clear", command=self._clear_output_directory,
                 bg="#f44336", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        
        # Queue section
        queue_frame = tk.LabelFrame(left_panel, text="File Queue", font=("Arial", 10, "bold"), padx=10, pady=10)
        queue_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Queue listbox with scrollbar
        queue_scroll = tk.Scrollbar(queue_frame)
        queue_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.queue_listbox = tk.Listbox(queue_frame, yscrollcommand=queue_scroll.set, 
                                       font=("Arial", 9), relief=tk.SUNKEN, borderwidth=1)
        self.queue_listbox.pack(fill=tk.BOTH, expand=True)
        self.queue_listbox.bind('<<ListboxSelect>>', self._on_queue_select)
        queue_scroll.config(command=self.queue_listbox.yview)
        
        # Queue count label
        self.queue_count_label = tk.Label(left_panel, text="Queue: 0 files", font=("Arial", 9), fg="#666")
        self.queue_count_label.pack(anchor=tk.W, padx=5)
        
        # Queue control buttons
        queue_btn_frame = tk.Frame(left_panel)
        queue_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(queue_btn_frame, text="Add Files", command=self._add_files_to_queue,
                 bg="#2196F3", fg="white", font=("Arial", 9, "bold")).pack(fill=tk.X, pady=2)
        
        tk.Button(queue_btn_frame, text="Remove Selected", command=self._remove_from_queue,
                 bg="#FF9800", fg="white", font=("Arial", 9)).pack(fill=tk.X, pady=2)
        
        tk.Button(queue_btn_frame, text="Clear Queue", command=self._clear_queue,
                 bg="#f44336", fg="white", font=("Arial", 9)).pack(fill=tk.X, pady=2)
        
        # Conversion buttons
        convert_btn_frame = tk.Frame(left_panel)
        convert_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.convert_batch_btn = tk.Button(convert_btn_frame, text="Convert All", 
                                          command=self._convert_batch,
                                          bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                                          padx=15, pady=10)
        self.convert_batch_btn.pack(fill=tk.X, pady=2)
        
        self.stop_btn = tk.Button(convert_btn_frame, text="Stop Conversion", 
                                 command=self._stop_conversion,
                                 bg="#f44336", fg="white", font=("Arial", 9),
                                 state=tk.DISABLED)
        self.stop_btn.pack(fill=tk.X, pady=2)
        
        # RIGHT PANEL - Preview
        right_panel = tk.Frame(main_container)
        main_container.add(right_panel, width=750)
        
        # Status bar
        status_frame = tk.Frame(right_panel)
        status_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        self.status_label = tk.Label(status_frame, text="Ready", bg="#e8f5e9", fg="#2e7d32", 
                                    font=("Arial", 9), relief=tk.SUNKEN, anchor=tk.W, padx=5, pady=3)
        self.status_label.pack(fill=tk.X)
        
        # Progress label
        self.progress_label = tk.Label(right_panel, text="", font=("Arial", 8), fg="#666")
        self.progress_label.pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        # Preview label
        preview_label = tk.Label(right_panel, text="Preview (Current File):", font=("Arial", 10, "bold"), padx=10)
        preview_label.pack(anchor=tk.W, pady=(10, 0))
        
        # Output text area
        text_frame = tk.Frame(right_panel, padx=10, pady=5)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Courier", 9),
                                                     bg="white", fg="#333", relief=tk.SUNKEN, borderwidth=1)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Footer
        footer = tk.Frame(right_panel, bg="#f0f0f0", padx=10, pady=5)
        footer.pack(fill=tk.X)
        tk.Label(footer, text="Bulk Conversion: Add files to queue → Select output directory → Click 'Convert All'",
                bg="#f0f0f0", font=("Arial", 8), fg="#999").pack(anchor=tk.W)
    
    def _select_output_directory(self):
        """Select the directory where all converted files will be saved."""
        directory = filedialog.askdirectory(title="Select Output Directory for Markdown Files")
        if directory:
            self.output_directory = Path(directory)
            self.dir_label.config(text=str(self.output_directory), fg="#333")
            self._update_status(f"Output directory set: {self.output_directory.name}", "#e8f5e9")
    
    def _clear_output_directory(self):
        """Clear the selected output directory."""
        self.output_directory = None
        self.dir_label.config(text="Not set", fg="#666")
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
            self._update_status(f"Added {len(files)} file(s) to queue", "#e8f5e9")
    
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
            self.output_text.insert(1.0, f"Selected: {self.current_file}\n\nClick 'Convert All' to process the queue.")
    
    def _remove_from_queue(self):
        """Remove selected file from queue."""
        selection = self.queue_listbox.curselection()
        if selection:
            idx = selection[0]
            removed = self.file_queue.pop(idx)
            self._update_queue_display()
            self._update_status(f"Removed: {removed.name}", "#fff3cd")
        else:
            messagebox.showwarning("No Selection", "Please select a file to remove from the queue.")
    
    def _clear_queue(self):
        """Clear all files from the queue."""
        if self.file_queue:
            if messagebox.askyesno("Clear Queue", "Are you sure you want to remove all files from the queue?"):
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
                progress_text = f"Converting {idx + 1}/{total}: {file_path.name}"
                self.root.after(0, self._update_progress, progress_text)
                
                status_text = f"Converting ({idx + 1}/{total}): {file_path.name}"
                def update_status_during_conversion():
                    self._update_status(status_text, "#fff3cd")
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
                    preview_text += f"\n\n... (truncated, total {len(result.text_content)} characters)"
                
                def update_preview(text=preview_text):
                    self.output_text.delete(1.0, tk.END)
                    self.output_text.insert(1.0, text)
                
                self.root.after(0, update_preview)
                
                successful += 1
                
            except Exception as e:
                failed += 1
                failed_files.append((file_path.name, str(e)))
                error_msg = f"Error converting {file_path.name}: {str(e)}"
                def show_error(msg=error_msg):
                    self._update_status(msg, "#ffebee")
                self.root.after(0, show_error)
        
        # Completion
        if self.is_converting:
            summary = f"✓ Batch conversion complete! {successful} converted, {failed} failed"
            self.root.after(0, self._update_progress, summary)
            
            def show_completion():
                self._update_status(summary, "#c8e6c9")
                messagebox.showinfo("Conversion Complete", 
                    f"Successfully converted: {successful}/{total} files\nSaved to:\n{self.output_directory}")
            
            self.root.after(0, show_completion)
        else:
            def show_stopped():
                self._update_status("Conversion stopped by user", "#fff3cd")
            self.root.after(0, show_stopped)
        
        # Re-enable buttons
        def enable_buttons():
            self.convert_batch_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
        
        self.root.after(0, enable_buttons)
        self.is_converting = False
    
    def _stop_conversion(self):
        """Stop the ongoing batch conversion."""
        self.is_converting = False
        self._update_status("Stopping conversion...", "#fff3cd")
    
    def _update_progress(self, message):
        """Update the progress label."""
        self.progress_label.config(text=message)
    
    def _update_status(self, message, bg_color="#e8f5e9"):
        """Update the status label."""
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
                self._update_status(f"Saved to: {file_path}", "#e8f5e9")
                messagebox.showinfo("Success", f"Markdown saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
                self._update_status(f"Error saving file: {str(e)}", "#ffebee")


def main():
    """Main entry point for the GUI."""
    root = tk.Tk()
    app = MarkItDownGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
