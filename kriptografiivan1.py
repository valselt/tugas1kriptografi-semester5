# Program Enkripsi dan Dekripsi dengan Vigenere, Playfair, dan Hill Cipher
# Tanpa library eksternal

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

def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None, None

# Fungsi untuk Hill Cipher
def hill_encrypt(plaintext, key):
    # Kunci harus berupa matriks 2x2 atau 3x3
    matrix_size = int(len(key) ** 0.5)
    if matrix_size * matrix_size != len(key):
        return "Invalid key length for Hill Cipher."
    key_matrix = create_key_matrix(key, matrix_size)
    
    # Memastikan panjang plainteks kelipatan matriks
    while len(plaintext) % matrix_size != 0:
        plaintext += 'x'
    
    ciphertext = ""
    for i in range(0, len(plaintext), matrix_size):
        block = plaintext[i:i + matrix_size]
        block_vector = [ord(char) - ord('a') for char in block]
        encrypted_vector = [(sum(key_matrix[row][col] * block_vector[col] for col in range(matrix_size)) % 26)
                            for row in range(matrix_size)]
        ciphertext += ''.join(chr(num + ord('a')) for num in encrypted_vector)
    return ciphertext

def hill_decrypt(ciphertext, key):
    matrix_size = int(len(key) ** 0.5)
    if matrix_size * matrix_size != len(key):
        return "Invalid key length for Hill Cipher."
    key_matrix = create_key_matrix(key, matrix_size)
    det = determinant(key_matrix)
    if det == 0:
        return "Key matrix is not invertible."
    inv_matrix = inverse_matrix(key_matrix, det, 26)
    
    plaintext = ""
    for i in range(0, len(ciphertext), matrix_size):
        block = ciphertext[i:i + matrix_size]
        block_vector = [ord(char) - ord('a') for char in block]
        decrypted_vector = [(sum(inv_matrix[row][col] * block_vector[col] for col in range(matrix_size)) % 26)
                            for row in range(matrix_size)]
        plaintext += ''.join(chr(num + ord('a')) for num in decrypted_vector)
    return plaintext

def create_key_matrix(key, size):
    return [[ord(key[i * size + j]) % 97 for j in range(size)] for i in range(size)]

def determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    elif len(matrix) == 3:
        return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
                matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
                matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))
    else:
        return 0

def inverse_matrix(matrix, det, mod):
    size = len(matrix)
    adjugate = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            minor = [[matrix[m][n] for n in range(size) if n != j] for m in range(size) if m != i]
            cofactor = determinant(minor) * ((-1) ** (i + j))
            adjugate[j][i] = cofactor % mod
    det_inv = pow(det, -1, mod)
    return [[(adjugate[i][j] * det_inv) % mod for j in range(size)] for i in range(size)]

# Fungsi untuk membaca dan menulis file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# Main program
def main():
    print("Pilih metode enkripsi/dekripsi:")
    print("1. Vigenere Cipher")
    print("2. Playfair Cipher")
    print("3. Hill Cipher")
    choice = input("Masukkan pilihan (1/2/3): ")

    mode = input("Pilih mode (encrypt/decrypt): ").strip().lower()
    if mode not in ["encrypt", "decrypt"]:
        print("Mode tidak valid.")
        return

    key = input("Masukkan kunci (minimal 12 karakter): ").strip()
    if len(key) < 12:
        print("Kunci harus minimal 12 karakter.")
        return

    input_choice = input("Masukkan input dari file (f) atau langsung (d): ").strip().lower()
    if input_choice == 'f':
        input_file = input("Masukkan path file input: ").strip()
        try:
            text = read_file(input_file)
        except FileNotFoundError:
            print("File tidak ditemukan.")
            return
    else:
        text = input("Masukkan teks: ").strip()

    if choice == "1":
        if mode == "encrypt":
            result = vigenere_encrypt(text, key)
        else:
            result = vigenere_decrypt(text, key)
    elif choice == "2":
        if mode == "encrypt":
            result = playfair_encrypt(text, key)
        else:
            result = playfair_decrypt(text, key)
    elif choice == "3":
        if mode == "encrypt":
            result = hill_encrypt(text, key)
        else:
            result = hill_decrypt(text, key)
    else:
        print("Pilihan tidak valid.")
        return

    output_choice = input("Simpan hasil ke file (y/n)? ").strip().lower()
    if output_choice == 'y':
        output_file = input("Masukkan path file output: ").strip()
        write_file(output_file, result)
        print("Hasil telah disimpan ke", output_file)
    else:
        print("Hasil:", result)

if __name__ == "__main__":
    main()
