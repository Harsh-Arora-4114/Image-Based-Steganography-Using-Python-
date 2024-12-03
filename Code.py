from tkinter import Tk, filedialog, simpledialog, messagebox
from PIL import Image, UnidentifiedImageError
import hashlib
from tkinter import Toplevel, Label, Entry, Button, StringVar, Frame

class PasswordDialog(Toplevel):
    def __init__(self, parent, prompt):
        Toplevel.__init__(self, parent)
        self.var = StringVar()
        self.create_widgets(prompt)
        self.wait_window(self)

    def create_widgets(self, prompt):
        # Window Title
        self.title("Enter Passcode")

        # Disable resizing
        self.resizable(False, False)

        # Prompt label
        self.label = Label(self, text=prompt)
        self.label.pack(pady=15, padx=20)

        # Entry for password
        self.entry = Entry(self, textvariable=self.var, show='*', width=30)
        self.entry.pack(pady=10, padx=20)
        self.entry.focus_set()

        # Button Frame for holding buttons
        self.button_frame = Frame(self)
        self.button_frame.pack(pady=15, padx=20)

        # Toggle Button to Show/Hide password
        self.toggle_button = Button(self.button_frame, text="Show", command=self.toggle_password, width=10)
        self.toggle_button.grid(row=0, column=0, padx=5)

        # OK Button to confirm input
        self.ok_button = Button(self.button_frame, text="OK", command=self.ok, width=10)
        self.ok_button.grid(row=0, column=1, padx=5)

        # Bind the Enter key to the OK button action
        self.bind('<Return>', lambda event=None: self.ok_button.invoke())

    def toggle_password(self):
        if self.entry['show'] == '*':
            self.entry['show'] = ''
            self.toggle_button.config(text="Hide")
        else:
            self.entry['show'] = '*'
            self.toggle_button.config(text="Show")

    def ok(self):
        self.user_input = self.var.get()
        self.destroy()


def select_file(prompt_text="Select a file"):
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=prompt_text)
    return file_path

def prompt_passcode(prompt_text="Enter the passcode"):
    root = Tk()
    root.withdraw()  # Hide the main root window
    dialog = PasswordDialog(root, prompt_text)
    return dialog.user_input


def message_to_bin(message):
    return ''.join(format(ord(i), '08b') for i in message)

def bin_to_message(binary_message):
    return ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

def file_to_bin(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        return ''.join(format(byte, '08b') for byte in content)

def bin_to_file(binary, output_file_path):
    byte_array = bytearray(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))
    with open(output_file_path, 'wb') as file:
        file.write(byte_array)

def hash_passcode(passcode):
    sha_signature = hashlib.sha256(passcode.encode()).hexdigest()
    return bin(int(sha_signature, 16))[2:].zfill(256)

def encode_image(img, data, passcode):
    binary_data = data
    passcode_hash = hash_passcode(passcode)

    binary_length = format(len(binary_data) + 256, '016b')  # SHA256 produces a 256-bit hash
    binary_data = binary_length + passcode_hash + binary_data 

    if len(binary_data) > img.width * img.height:
        print("Data is too long for the image!")
        return False

    encoded = img.copy()
    width, height = img.size
    idx = 0

    for y in range(height):
        for x in range(width):
            pixel = list(encoded.getpixel((x, y)))
            pixel[0] = (pixel[0] & ~1) | int(binary_data[idx])
            encoded.putpixel((x, y), tuple(pixel))
            idx += 1
            if idx == len(binary_data):
                return encoded

def decode_image(img, passcode):
    width, height = img.size
    binary_data = ""

    for i in range(16):
        binary_data += str(img.getpixel((i%width, i//width))[0] & 1)

    data_len = int(binary_data, 2)
    binary_data = ""

    for i in range(16, 16+256):
        binary_data += str(img.getpixel((i%width, i//width))[0] & 1)

    extracted_hash = binary_data
    if extracted_hash != hash_passcode(passcode):
        print("Wrong passcode entered!")
        return None

    binary_data = ""
    for i in range(16+256, 16+256+data_len-256):
        binary_data += str(img.getpixel((i%width, i//width))[0] & 1)

    return binary_data

def main():
    try:
        action = input("Choose action (encode/decode): ").strip().lower()
        if action not in ["encode", "decode"]:
            print("Invalid action chosen. Exiting.")
            exit()
        
        embedding_type = input("Choose embedding type (message/file): ").strip().lower()
        if embedding_type not in ["message", "file"]:
            print("Invalid embedding type chosen. Exiting.")
            exit()
        
        if action == "encode":
            try:
                original_image_path = select_file("Upload the base image")
                original_image = Image.open(original_image_path)
            except UnidentifiedImageError:
                print("Error: Uploaded file is not a recognized image format.")
                return
            except Exception as e:
                print(f"Error: {e}")
                return

            if embedding_type == "message":
                message = input("Enter the message to encode: ")
                data_to_embed = message_to_bin(message)
            elif embedding_type == "file":
                try:
                    file_path = select_file("Upload the file to encode")
                    data_to_embed = file_to_bin(file_path)
                except Exception as e:
                    print(f"Error reading file: {e}")
                    return

            passcode = prompt_passcode("Enter a passcode to lock the encoded data:")
            encoded_image = encode_image(original_image, data_to_embed, passcode)

            if encoded_image:
                output_image_name = input("Enter the desired name for the encoded image (e.g., output.png): ")
                encoded_image.save(output_image_name)
                print(f"Encoded image saved as {output_image_name}!")
            else:
                print("Failed to encode the image.")

        elif action == "decode":
            try:
                encoded_image_path = select_file("Upload the encoded image")
                encoded_image = Image.open(encoded_image_path)
            except UnidentifiedImageError:
                print("Error: Uploaded file is not a recognized image format.")
                return
            except Exception as e:
                print(f"Error: {e}")
                return

            passcode = prompt_passcode("Enter the passcode to unlock the encoded data:")
            binary_data = decode_image(encoded_image, passcode)

            if not binary_data:
                print("Failed to decode the image.")
                return

            if embedding_type == "message":
                extracted_data = bin_to_message(binary_data)
                print(f"Decoded message: {extracted_data}")
            elif embedding_type == "file":
                try:
                    output_file_name = input("Enter the desired name for the extracted file (e.g., document.txt): ")
                    bin_to_file(binary_data, output_file_name)
                    print(f"File has been extracted and saved as {output_file_name}!")
                except Exception as e:
                    print(f"Error saving file: {e}")

        else:
            print("Invalid action chosen. Exiting.")
            exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
