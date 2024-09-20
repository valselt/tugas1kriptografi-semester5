import tkinter as tk
from tkinter import filedialog, messagebox

# Fungsi untuk Vigenere Cipher
def vigenere_encrypt(plaintext, key):
    key = key.lower()
    ciphertext = ""
    j = 0
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            shift = (ord(plaintext[i].lower()) + ord(key[j % len(key)].lower()) - 2 * ord('a')) % 26
            ciphertext += chr(shift + ord('a'))
            j += 1
        else:
            ciphertext += plaintext[i]
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    key = key.lower()
    plaintext = ""
    j = 0
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            shift = (ord(ciphertext[i].lower()) - ord(key[j % len(key)].lower()) + 26) % 26
            plaintext += chr(shift + ord('a'))
            j += 1
        else:
            plaintext += ciphertext[i]
    return plaintext

# Fungsi untuk Playfair Cipher
def create_playfair_matrix(key):
    alphabet = "abcdefghiklmnopqrstuvwxyz"  # Tidak termasuk 'j'
    matrix = []
    key = key.lower().replace("j", "i")
    for char in key:
        if char not in matrix and char in alphabet:
            matrix.append(char)
    for char in alphabet:
        if char not in matrix:
            matrix.append(char)
    return [matrix[i:i + 5] for i in range(0, len(matrix), 5)]

def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None, None

def playfair_encrypt(plaintext, key):
    matrix = create_playfair_matrix(key)
    plaintext = plaintext.lower().replace("j", "i")
    plaintext_pairs = []
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        b = 'x' if i + 1 == len(plaintext) else plaintext[i + 1]
        if a == b:
            plaintext_pairs.append(a + 'x')
            i += 1
        else:
            plaintext_pairs.append(a + b)
            i += 2
    ciphertext = ""
    for a, b in plaintext_pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:
            ciphertext += matrix[row1][(col1 + 1) % 5]
            ciphertext += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += matrix[(row1 + 1) % 5][col1]
            ciphertext += matrix[(row2 + 1) % 5][col2]
        else:
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]
    return ciphertext

def playfair_decrypt(ciphertext, key):
    matrix = create_playfair_matrix(key)
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:
            plaintext += matrix[row1][(col1 - 1) % 5]
            plaintext += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]
    return plaintext

# Fungsi untuk Hill Cipher (disederhanakan)
def hill_encrypt(plaintext, key):
    # Implementasi Hill Cipher akan ditambahkan di sini
    return "Hill cipher belum diimplementasikan."

def hill_decrypt(ciphertext, key):
    # Implementasi Hill Cipher akan ditambahkan di sini
    return "Hill cipher belum diimplementasikan."

# Fungsi untuk mengencrypt atau mendekripsi
def process():
    method = method_var.get()
    mode = mode_var.get()
    key = key_entry.get()
    text = input_text.get("1.0", tk.END).strip()

    if len(key) < 12:
        messagebox.showerror("Error", "Kunci harus minimal 12 karakter.")
        return

    if method == "Vigenere":
        result = vigenere_encrypt(text, key) if mode == "Encrypt" else vigenere_decrypt(text, key)
    elif method == "Playfair":
        result = playfair_encrypt(text, key) if mode == "Encrypt" else playfair_decrypt(text, key)
    else:
        result = hill_encrypt(text, key) if mode == "Encrypt" else hill_decrypt(text, key)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

# GUI Setup
root = tk.Tk()
root.title("Cipher Encryption/Decryption")

method_var = tk.StringVar(value="Vigenere")
mode_var = tk.StringVar(value="Encrypt")

tk.Label(root, text="Metode:").grid(row=0, column=0)
tk.OptionMenu(root, method_var, "Vigenere", "Playfair", "Hill").grid(row=0, column=1)

tk.Label(root, text="Mode:").grid(row=1, column=0)
tk.OptionMenu(root, mode_var, "Encrypt", "Decrypt").grid(row=1, column=1)

tk.Label(root, text="Kunci:").grid(row=2, column=0)
key_entry = tk.Entry(root)
key_entry.grid(row=2, column=1)

tk.Label(root, text="Input:").grid(row=3, column=0)
input_text = tk.Text(root, height=10, width=50)
input_text.grid(row=3, column=1)

tk.Button(root, text="Proses", command=process).grid(row=4, columnspan=2)

tk.Label(root, text="Output:").grid(row=5, column=0)
output_text = tk.Text(root, height=10, width=50)
output_text.grid(row=5, column=1)

root.mainloop()
