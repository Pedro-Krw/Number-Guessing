def encode_message(command, data):
    return f"{command}:{data}".encode()

def decode_message(message_bytes):
    decoded = message_bytes.decode()
    parts = decoded.split(":", 1)
    return parts[0], parts[1] if len(parts) > 1 else ""
