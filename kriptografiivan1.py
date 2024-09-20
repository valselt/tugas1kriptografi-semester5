import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

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
    alphabet = "abcdefghiklmnopqrstuvwxyz"
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

def process(method, mode, key, text):
    if len(key) < 12:
        messagebox.showerror("Error", "Kunci harus minimal 12 karakter.")
        return

    if method == "Vigenere":
        result = vigenere_encrypt(text, key) if mode == "Encrypt" else vigenere_decrypt(text, key)
    elif method == "Playfair":
        result = playfair_encrypt(text, key) if mode == "Encrypt" else playfair_decrypt(text, key)

    return result

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    return ""

def main():
    method = simpledialog.askstring("Metode Enkripsi", "Pilih metode (Vigenere/Playfair):")
    if method not in ["Vigenere", "Playfair"]:
        messagebox.showerror("Error", "Metode tidak valid.")
        return

    mode = simpledialog.askstring("Mode", "Pilih mode (Encrypt/Decrypt):")
    if mode not in ["Encrypt", "Decrypt"]:
        messagebox.showerror("Error", "Mode tidak valid.")
        return

    key = simpledialog.askstring("Kunci", "Masukkan kunci (minimal 12 karakter):")
    if key is None or len(key) < 12:
        messagebox.showerror("Error", "Kunci tidak valid.")
        return

    input_choice = simpledialog.askstring("Input", "Masukkan input dari file (f) atau langsung (l):")
    if input_choice == 'f':
        text = upload_file()
        if not text:
            messagebox.showerror("Error", "Tidak ada konten dalam file.")
            return
    elif input_choice == 'l':
        text = simpledialog.askstring("Input Teks", "Masukkan teks:")
        if text is None:
            return
    else:
        messagebox.showerror("Error", "Pilihan input tidak valid.")
        return

    result = process(method, mode, key, text)

    if result:
        save_choice = messagebox.askyesno("Simpan Hasil", "Apakah Anda ingin menyimpan hasilnya ke file?")
        if save_choice:
            output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if output_file:
                with open(output_file, 'w') as file:
                    file.write(result)
                messagebox.showinfo("Info", "Hasil telah disimpan.")
            else:
                messagebox.showerror("Error", "Gagal menyimpan hasil.")
        else:
            messagebox.showinfo("Hasil", f"Hasil:\n{result}")

# GUI Setup
root = tk.Tk()
root.withdraw()  # Sembunyikan jendela utama
main()
root.mainloop()
