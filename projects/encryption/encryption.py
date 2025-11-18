#!/usr/bin/env python3
"""
Encryption Module - Python Wrapper for AES-256 Encryption
AI-Generated Implementation
Supports multiple encryption algorithms and block modes
"""

import os
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import hashlib

class EncryptionEngine:
    """Main encryption engine supporting multiple algorithms"""
    
    def __init__(self, algorithm='AES-256'):
        self.algorithm = algorithm
        self.backend = default_backend()
        self.block_size = 16  # 128 bits
        
    def generate_key(self, passphrase):
        """Generate AES key from passphrase using SHA-256"""
        key = hashlib.sha256(passphrase.encode()).digest()
        return key
    
    def generate_iv(self):
        """Generate random initialization vector"""
        return os.urandom(self.block_size)
    
    def encrypt_aes256(self, plaintext, key, iv=None):
        """Encrypt data using AES-256-CBC"""
        if iv is None:
            iv = self.generate_iv()
        
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        
        # Add PKCS7 padding
        padding_length = self.block_size - (len(plaintext) % self.block_size)
        padded_plaintext = plaintext + bytes([padding_length]) * padding_length
        
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return iv + ciphertext
    
    def decrypt_aes256(self, ciphertext, key):
        """Decrypt AES-256-CBC encrypted data"""
        iv = ciphertext[:self.block_size]
        encrypted_data = ciphertext[self.block_size:]
        
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Remove PKCS7 padding
        padding_length = padded_plaintext[-1]
        plaintext = padded_plaintext[:-padding_length]
        return plaintext
    
    def encrypt_text(self, text, passphrase):
        """Encrypt plain text with passphrase"""
        key = self.generate_key(passphrase)
        plaintext_bytes = text.encode('utf-8')
        ciphertext = self.encrypt_aes256(plaintext_bytes, key)
        return ciphertext.hex()
    
    def decrypt_text(self, hex_ciphertext, passphrase):
        """Decrypt ciphertext with passphrase"""
        key = self.generate_key(passphrase)
        ciphertext = bytes.fromhex(hex_ciphertext)
        plaintext_bytes = self.decrypt_aes256(ciphertext, key)
        return plaintext_bytes.decode('utf-8')

# Module initialization
if __name__ == '__main__':
    engine = EncryptionEngine('AES-256')
    test_message = "Hello, Encryption!"
    test_passphrase = "SecurePassword123"
    
    encrypted = engine.encrypt_text(test_message, test_passphrase)
    print(f"Encrypted: {encrypted}")
    
    decrypted = engine.decrypt_text(encrypted, test_passphrase)
    print(f"Decrypted: {decrypted}")

# Written by: AI Agents
# License: MIT
