# Image Steganography Tool

## Overview
This is a Python-based image steganography tool that allows users to encode and decode messages or files into images using the Least Significant Bit (LSB) method. The encoded data is protected with a passcode, ensuring security and confidentiality.

## Features
- **Encode messages or files** into images.
- **Decode hidden data** from images.
- **Passcode protection** using SHA-256 hashing.
- **Graphical User Interface (GUI)** for passcode entry.
- **Supports multiple image formats** (PNG, JPG, BMP, etc.).

## Requirements
Make sure you have the following dependencies installed:

```bash
pip install pillow
```

## How It Works
### Encoding Process
1. Select the image to be used as a carrier.
2. Choose whether to embed a message or a file.
3. Enter the message or select the file to embed.
4. Enter a passcode to secure the hidden data.
5. Save the new encoded image.

### Decoding Process
1. Select the encoded image.
2. Enter the correct passcode.
3. Retrieve the hidden message or extract the hidden file.

## Usage
Run the script using the following command:

```bash
python script.py
```

Follow the on-screen instructions to encode or decode data.

## Example
### Encoding a Message
```plaintext
Choose action (encode/decode): encode
Choose embedding type (message/file): message
Upload the base image
Enter the message to encode: Hello, world!
Enter a passcode to lock the encoded data:
Enter the desired name for the encoded image (e.g., output.png): secret.png
Encoded image saved as secret.png!
```

### Decoding a Message
```plaintext
Choose action (encode/decode): decode
Choose embedding type (message/file): message
Upload the encoded image
Enter the passcode to unlock the encoded data:
Decoded message: Hello, world!
```

## Error Handling
- If the image is not a valid format, an error message will be displayed.
- If the entered passcode is incorrect, the decoding will fail.
- If the data is too large for the image, encoding will not proceed.

## Contributions
Feel free to fork this repository, submit issues, and create pull requests to improve the project.

## Author
Developed by Harsh Arora.
