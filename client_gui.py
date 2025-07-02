import socket
import threading
import tkinter as tk
from tkinter import messagebox
from protocol import encode_message, decode_message

HOST = 'localhost'
PORT = 5555

class GuessingGameClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Tebak Angka Multiplayer")

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            print("[DEBUG] Berhasil terhubung ke server")
        except Exception as e:
            messagebox.showerror("Koneksi Gagal", f"Gagal terhubung ke server: {e}")
            root.destroy()
            return

        self.label = tk.Label(root, text="Masukkan tebakan (1-100):")
        self.label.pack(pady=5)

        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)

        self.email_label = tk.Label(root, text="Email kamu:")
        self.email_label.pack(pady=5)

        self.email_entry = tk.Entry(root)
        self.email_entry.pack(pady=5)

        self.button = tk.Button(root, text="Kirim Tebakan", command=self.send_guess)
        self.button.pack(pady=10)

        self.result_text = tk.Text(root, height=10, width=50, state='disabled')
        self.result_text.pack(pady=5)

        # Mulai thread untuk mendengarkan dari server
        self.listen_thread = threading.Thread(target=self.listen_server, daemon=True)
        self.listen_thread.start()

    def send_guess(self):
        guess = self.entry.get().strip()
        email = self.email_entry.get().strip()

        if not guess.isdigit():
            messagebox.showerror("Error", "Tebakan harus angka.")
            return
        if email == "":
            messagebox.showerror("Error", "Email tidak boleh kosong.")
            return

        try:
            message = f"{guess},{email}"
            print(f"[DEBUG] Siap encode dan kirim: {message}")
            msg = encode_message("GUESS", message)
            self.sock.send(msg)
            print("[DEBUG] Tebakan berhasil dikirim")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengirim tebakan: {e}")

    def listen_server(self):
        while True:
            try:
                msg = self.sock.recv(1024)
                if not msg:
                    print("[DEBUG] Server menutup koneksi.")
                    break
                command, data = decode_message(msg)
                print(f"[DEBUG] Diterima dari server → Command: {command}, Data: {data}")

                self.result_text.configure(state='normal')
                self.result_text.insert(tk.END, f"{data}\n")
                self.result_text.configure(state='disabled')
                self.result_text.see(tk.END)

                if "Tebakan benar" in data:
                    messagebox.showinfo("Selamat!", "Tebakan kamu benar!")
                    break
            except Exception as e:
                print(f"[ERROR] {e}")
                break

        self.sock.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = GuessingGameClient(root)
    root.mainloop()
