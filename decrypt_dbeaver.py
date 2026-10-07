import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

DBEAVER_KEY = bytes([186, 187, 74, 159, 127, 18, 130, 217, 46, 45, 46, 190, 228, 159, 188, 79])
cred_path = r'C:\Users\tanko\AppData\Roaming\DBeaverData\workspace6\General\.dbeaver\credentials-config.json'

try:
    with open(cred_path, 'rb') as f:
        raw_bytes = f.read()

    if len(raw_bytes) > 16:
        iv = raw_bytes[:16]
        ciphertext = raw_bytes[16:]
        cipher = Cipher(algorithms.AES(DBEAVER_KEY), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()
        
        # unpad
        pad = decrypted[-1]
        if isinstance(pad, int) and pad < 16:
            decrypted = decrypted[:-pad]
            
        dec_str = decrypted.decode('utf-8', errors='ignore')
        creds = json.loads(dec_str)
        target_id = "postgres-jdbc-194a25a03a4-3b7dc91aa0b452b6"
        if target_id in creds:
            print("FOUND TARGET CREDS:", creds[target_id])
        else:
            for k, v in creds.items():
                if '194a25a03a4' in k:
                    print(f"Key {k}: {v}")
except Exception as e:
    print("Decryption failed:", e)
