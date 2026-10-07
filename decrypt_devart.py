# Devart password decryption
# In Devart components, EncryptedPassword is hex pairs where each char is inverted or XORed with a constant or running key

def decrypt_devart(enc_hex):
    # Split into 4-char chunks (e.g. CEFF, CDFF)
    chunks = [enc_hex[i:i+4] for i in range(0, len(enc_hex), 4)]
    bytes_val = [int(c[:2], 16) for c in chunks] # take low byte
    
    # Try common Devart XOR keys (like 0xAA, 0x55, 0xFF, or running keys)
    print("Chunks count:", len(chunks))
    print("Bytes:", [hex(b) for b in bytes_val])
    
    # In Devart: char_code = not byte or byte xor constant
    # Let's test with various XOR keys from 0 to 255:
    candidates = []
    for key in range(256):
        res = "".join(chr(b ^ key) for b in bytes_val)
        if all(32 <= ord(c) <= 126 for c in res):
            candidates.append((key, res))
    return candidates

p1 = "CEFFCDFF8AFF8FFF9BFF9EFF8BFF9AFFCCFFCBFF"
p2 = "AFFFA6FF85FFBBFFA6FFB6FF9AFF8AFF8AFFCBFF8FFFABFF99FFC6FFB5FF8CFF"

print("P1 candidates:")
for k, text in decrypt_devart(p1):
    print(f"  Key {k} (0x{k:02x}): {text}")

print("\nP2 candidates:")
for k, text in decrypt_devart(p2):
    print(f"  Key {k} (0x{k:02x}): {text}")
