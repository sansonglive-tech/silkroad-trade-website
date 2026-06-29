# -*- coding: utf-8 -*-
"""Test shapes in header for page border"""

import win32com.client

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

doc = word.Documents.Add()

# Test adding shapes in the primary header
section = doc.Sections(1)
section.PageSetup.DifferentFirstPageHeaderFooter = True

hdr = section.Headers(1)  # Primary header
hdr.LinkToPrevious = False
hdr.Range.Text = ""

# Try to add decorative shapes
try:
    pw = doc.PageSetup.PageWidth
    ph = doc.PageSetup.PageHeight
    
    # Add a thin rectangle as page border in header background
    # Width and height as full page
    shape = hdr.Shapes.AddShape(
        1,   # msoShapeRectangle = 1
        36,  # Left - inset from edge
        30,  # Top - near top margin
        pw - 72,  # Width - full width minus insets
        ph - 60   # Height - full height minus insets
    )
    shape.Fill.Transparency = 1.0  # No fill
    shape.Line.ForeColor.RGB = 0x55B1C9  # Gold
    shape.Line.Weight = 1.5
    shape.Line.DashStyle = 1  # Solid
    shape.WrapFormat.Type = 3  # Behind text
    print("  Shape border added successfully")
    
except Exception as e:
    print(f"  Error adding border shape: {e}")

doc.Close(False)
word.Quit()
print("Done")
