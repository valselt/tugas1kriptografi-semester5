global key,input_label  # Menyimpan key ke variabel global
    key = simpledialog.askstring("Kunci", "Masukkan kunci (minimal 12 karakter):")
    if key is None or len(key) < 12:
        messagebox.showerror("Error", "Kunci tidak valid.")
        return