import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import numpy as np

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
        if not a.isalpha():
            i += 1
            continue
        
        if i + 1 < len(plaintext):
            b = plaintext[i + 1]
            if a == b:  # Jika karakter sama, gunakan 'x'
                b = 'x'
                plaintext_pairs.append(a + b)
                i += 1  # Lewati satu karakter
            else:
                plaintext_pairs.append(a + b)
                i += 2  # Lewati dua karakter
        else:
            # Jika hanya satu karakter tersisa, tambahkan 'x'
            plaintext_pairs.append(a + 'x')
            i += 1

    ciphertext = ""
    for item in plaintext_pairs:
        a, b = item
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 is not None and row2 is not None:
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
    i = 0

    while i < len(ciphertext):
        a = ciphertext[i]
        if not a.isalpha():
            plaintext += a  # Pertahankan karakter non-alfabet
            i += 1
            continue
        
        if i + 1 < len(ciphertext):
            b = ciphertext[i + 1]
        else:
            b = 'x'  # Jika hanya ada satu huruf, gantikan dengan 'x'

        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 is not None and row2 is not None:
            if row1 == row2:
                plaintext += matrix[row1][(col1 - 1) % 5]
                plaintext += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                plaintext += matrix[(row1 - 1) % 5][col1]
                plaintext += matrix[(row2 - 1) % 5][col2]
            else:
                plaintext += matrix[row1][col2]
                plaintext += matrix[row2][col1]

        i += 2  # Lewati dua karakter

    return plaintext


# Fungsi untuk Hill Cipher
def hill_encrypt(plaintext, key):
    key_matrix = np.array(key).reshape(2, 2)
    plaintext_vector = np.array([ord(c) - ord('a') for c in plaintext.lower() if c.isalpha()]).reshape(-1, 2)
    ciphertext_vector = (plaintext_vector @ key_matrix) % 26
    ciphertext = ''.join(chr(c + ord('a')) for c in ciphertext_vector.flatten())
    return ciphertext

def hill_decrypt(ciphertext, key):
    key_matrix = np.array(key).reshape(2, 2)
    det = int(np.round(np.linalg.det(key_matrix))) % 26
    det_inv = pow(det, -1, 26)
    adjugate_matrix = np.round(det * np.linalg.inv(key_matrix)).astype(int) % 26
    inverse_key_matrix = (det_inv * adjugate_matrix) % 26
    ciphertext_vector = np.array([ord(c) - ord('a') for c in ciphertext.lower() if c.isalpha()]).reshape(-1, 2)
    plaintext_vector = (ciphertext_vector @ inverse_key_matrix) % 26
    plaintext = ''.join(chr(p + ord('a')) for p in plaintext_vector.flatten())
    return plaintext

def process(method, mode, key, text):
    if len(key) != 4 or not all(c.isalpha() for c in key):
        messagebox.showerror("Error", "Kunci harus terdiri dari 4 huruf.")
        return

    key_matrix = np.array([ord(c) - ord('a') for c in key]).reshape(2, 2)  # Membentuk matriks 2x2 dari kunci

    if method == "Vigenere":
        result = vigenere_encrypt(text, key) if mode == "Encrypt" else vigenere_decrypt(text, key)
    elif method == "Playfair":
        result = playfair_encrypt(text, key) if mode == "Encrypt" else playfair_decrypt(text, key)
    elif method == "Hill":
        result = hill_encrypt(text, key_matrix) if mode == "Encrypt" else hill_decrypt(text, key_matrix)

    return result


def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    return ""

def run_encryption(method, key, text):
    result = process(method, "Encrypt", key, text)
    if result:
        save_choice = messagebox.askyesno("Simpan Hasil", "Apakah Anda ingin menyimpan hasilnya ke file?")
        if save_choice:
            output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if output_file:
                with open(output_file, 'w') as file:
                    file.write(result)
                messagebox.showinfo("Info", "Hasil telah disimpan.")
        else:
            # Tampilkan hasil enkripsi hanya jika "Tidak" dipilih
            messagebox.showinfo("Hasil Enkripsi", f"Hasil: {result}")

        # Tambahkan popup untuk mengulang atau keluar
        repeat = messagebox.askyesno("Ulang Program", "Apakah Anda ingin mengulang program?")
        if repeat:
            reset_program()  # Fungsi untuk mengatur ulang tampilan
        else:
            root.quit()  # Keluar dari aplikasi

def run_decryption(method, key, text):
    result = process(method, "Decrypt", key, text)
    if result:
        save_choice = messagebox.askyesno("Simpan Hasil", "Apakah Anda ingin menyimpan hasilnya ke file?")
        if save_choice:
            output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if output_file:
                with open(output_file, 'w') as file:
                    file.write(result)
                messagebox.showinfo("Info", "Hasil telah disimpan.")
        else:
            # Tampilkan hasil dekripsi hanya jika "Tidak" dipilih
            messagebox.showinfo("Hasil Dekripsi", f"Hasil: {result}")

        # Tambahkan popup untuk mengulang atau keluar
        repeat = messagebox.askyesno("Ulang Program", "Apakah Anda ingin mengulang program?")
        if repeat:
            reset_program()  # Fungsi untuk mengatur ulang tampilan
        else:
            root.quit()  # Keluar dari aplikasi


def upload_file_action(method):
    text = upload_file()  # Mengambil konten dari file
    if not text:
        messagebox.showerror("Error", "Tidak ada konten dalam file.")
        return
    
    choose_mode(method, text)  # Panggil fungsi untuk memilih mode
 # Panggil fungsi untuk memilih mode

def input_text_action(method):
    global text
    text = simpledialog.askstring("Input Teks", "Masukkan teks:")
    if text is None:
        return
    choose_mode(method, text)  # Panggil fungsi untuk memilih mode
  # Panggil fungsi untuk memilih mode

def choose_mode(method, text):
    # Menghapus pilihan input sebelumnya
    for widget in root.pack_slaves():
        if isinstance(widget, tk.Button):
            widget.destroy()

    # Hapus input_label jika ada
    if input_label:
        input_label.pack_forget()

    # Tampilkan label untuk memilih mode
    mode_label = tk.Label(root, text="Pilih mode (Encrypt/Decrypt)", font=("Arial", 12))
    mode_label.pack(pady=10)

    # Tombol untuk Enkripsi
    encrypt_button = tk.Button(root, text="Encrypt", command=lambda: run_encryption(method, key, text))
    encrypt_button.pack(pady=5)

    # Tombol untuk Dekripsi
    decrypt_button = tk.Button(root, text="Decrypt", command=lambda: run_decryption(method, key, text))
    decrypt_button.pack(pady=5)


def choose_method(method):
    global key,input_label  # Menyimpan key ke variabel global
    key = simpledialog.askstring("Kunci", "Masukkan kunci (minimal 12 karakter):")
    if key is None or len(key) < 12:
        messagebox.showerror("Error", "Kunci tidak valid.")
        return

    # Menghapus pilihan sebelumnya
    for widget in root.pack_slaves():
        if isinstance(widget, tk.Button):
            widget.destroy()

    # Hapus welcome_label
    if welcome_label :
        welcome_label.pack_forget()

    # Menampilkan label untuk memilih input
    input_label = tk.Label(root, text="Masukkan input dari file (f) atau langsung (l):", font=("Arial", 12))
    input_label.pack(pady=10)

    # Tombol untuk memilih input
    upload_button = tk.Button(root, text="Upload File", command=lambda: upload_file_action(method))
    upload_button.pack(side=tk.LEFT, padx=5)

    input_button = tk.Button(root, text="Input Langsung", command=lambda: input_text_action(method))
    input_button.pack(side=tk.LEFT, padx=5)

def reset_program():
    for widget in root.pack_slaves():
        widget.destroy()  # Hapus semua widget di jendela
    main()  # Jalankan kembali fungsi main untuk memulai ulang aplikasi


def main():
    global root, welcome_label  # Menandai root sebagai variabel global
    root = tk.Tk()
    root.title("Kriptografi")
    
    welcome_label = tk.Label(root, text="Pilih Cipher yang tersedia", font=("Arial", 14))
    welcome_label.pack(pady=20)
    
    methods = ["Vigenere", "Playfair", "Hill"]
    for method in methods:
        btn = tk.Button(root, text=method, command=lambda m=method: choose_method(m))
        btn.pack(pady=10)

    root.mainloop()

# Menjalankan aplikasi
main()
