import socket
import threading
import random
from protocol import encode_message, decode_message
from email_sender import send_email

HOST = 'localhost'
PORT = 5555

clients = []
secret_number = random.randint(1, 100)
winner_email = None

def handle_client(conn, addr):
    global winner_email
    print(f"[NEW CONNECTION] {addr} connected.")
    print(f"[DEBUG] Angka rahasia saat ini: {secret_number}")
    
    conn.send(encode_message("INFO", "Selamat datang! Coba tebak angka 1-100."))

    try:
        while True:
            msg = conn.recv(1024)
            if not msg:
                print(f"[DEBUG] Client {addr} memutuskan koneksi.")
                break

            print(f"[RECEIVED] Raw from {addr}: {msg}")
            command, data = decode_message(msg)
            print(f"[DEBUG] From {addr} — Command: {command}, Data: {data}")

            if command == "GUESS":
                try:
                    guess, email = data.split(",")
                    guess = int(guess)
                    print(f"[DEBUG] Parsed Guess: {guess}, Email: {email}")
                except Exception as e:
                    print(f"[ERROR] Failed to parse guess/email: {e}")
                    conn.send(encode_message("ERROR", "Format tebakan salah."))
                    continue

                if guess < secret_number:
                    print(f"[INFO] {addr} tebak {guess} → terlalu kecil")
                    conn.send(encode_message("RESULT", "Terlalu kecil."))
                elif guess > secret_number:
                    print(f"[INFO] {addr} tebak {guess} → terlalu besar")
                    conn.send(encode_message("RESULT", "Terlalu besar."))
                else:
                    print(f"[INFO] {addr} tebak {guess} → BENAR!")
                    conn.send(encode_message("RESULT", "Tebakan benar!"))
                    winner_email = email
                    broadcast_msg = f"Pemain {addr} menang dengan tebakan {guess}!"
                    print(f"[BROADCAST] {broadcast_msg}")
                    broadcast(encode_message("INFO", broadcast_msg))

                    print("[DEBUG] Memanggil fungsi send_email...")
                    send_email(email)
                    print("[DEBUG] Fungsi send_email selesai dipanggil.")
                    break
    except Exception as e:
        print(f"[ERROR] Exception in handle_client: {e}")
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except Exception as e:
            print(f"[ERROR] Failed to broadcast to a client: {e}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER RUNNING] Listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        print(f"[ACCEPTED] Connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
