#!/usr/bin/env python3
"""Convert image to base64 data URI for embedding in HTML."""
import base64
import sys

# Read the image file
with open('wechat_qr.png', 'rb') as f:
    image_data = f.read()

# Convert to base64
base64_data = base64.b64encode(image_data).decode('utf-8')

# Create data URI
data_uri = f'data:image/png;base64,{base64_data}'

# Print first 200 chars and total length
print(f"Base64 length: {len(data_uri)} characters")
print(f"\nFirst 200 chars:\n{data_uri[:200]}...")
print(f"\n\nFull data URI (copy this):\n{data_uri}")
