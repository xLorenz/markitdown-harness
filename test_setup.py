#!/usr/bin/env python3
"""Test script to verify MarkItDown is properly installed."""

try:
    import markitdown
    print("✓ MarkItDown imported successfully")
    
    md = markitdown.MarkItDown()
    print("✓ MarkItDown converter initialized")
    
    print("\n✓ Setup is complete and working!")
    print("\nYou can now run: python gui_harness.py")
    print("Or on Windows: double-click run.bat")
    
except ImportError as e:
    print(f"✗ Error: {e}")
    print("\nTo fix, run:")
    print("  pip install -e packages/markitdown[all]")
