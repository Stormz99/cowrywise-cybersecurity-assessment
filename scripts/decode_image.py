#!/usr/bin/env python3
"""
Base64 Decoder for image.txt for CowryWise Cybersecurity Internship Assessment
"""

import base64
from pathlib import Path

def log(msg):
    print(f"[*] {msg}")

def log_success(msg):
    print(f"[+] {msg}")

def log_error(msg):
    print(f"[-] {msg}")

def find_input_file(filename='image.txt'):
    """Search current and parent directory for the input file"""
    current = Path.cwd() / filename
    parent = Path.cwd().parent / filename
    if current.exists():
        return current
    elif parent.exists():
        return parent
    else:
        return None

def attempt_base64_decode(input_file):
    log(f"Attempting Base64 decode for: {input_file}")
    try:
        with open(input_file, 'r') as f:
            content = f.read()
        clean_content = ''.join(content.split())
        decoded = base64.b64decode(clean_content)
        log_success(f"Base64 decode successful: {len(decoded)} bytes")
        return decoded
    except Exception as e:
        log_error(f"Base64 decode failed: {e}")
        return None

def detect_file_type(data):
    """Detect file type based on magic bytes"""
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return 'PNG image'
    elif data[:3] == b'\xff\xd8\xff':
        return 'JPEG image'
    elif data[:4] == b'GIF8':
        return 'GIF image'
    elif data[:4] == b'%PDF':
        return 'PDF document'
    else:
        return 'Unknown'

def save_output(data, filename='decoded_image.bin'):
    """Save decoded data to output folder"""
    output_dir = Path('decoded_outputs')
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / filename
    output_path.write_bytes(data)
    log_success(f"Saved decoded file to: {output_path}")
    log(f"Detected file type: {detect_file_type(data)}")
    return output_path

def main():
    input_file = find_input_file()
    if not input_file:
        log_error("image.txt not found in current or parent directory")
        return

    log(f"Processing: {input_file}")
    log(f"File size: {input_file.stat().st_size} bytes\n")

    decoded = attempt_base64_decode(input_file)
    if decoded:
        save_output(decoded, 'decoded_image.bin')

    log("\nDone!")

if __name__ == '__main__':
    main()
