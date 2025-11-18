#!/usr/bin/env python3
"""
File Encryption Utility
Encrypt and decrypt files with support for multiple file types
AI-Generated Implementation
"""

import os
import sys
from pathlib import Path
from encryption import EncryptionEngine

class FileEncryptor:
    """File encryption/decryption utility"""
    
    SUPPORTED_FORMATS = ['.txt', '.pdf', '.docx', '.jpg', '.png', '.zip', '.py', '.cpp']
    
    def __init__(self, passphrase):
        self.engine = EncryptionEngine('AES-256')
        self.passphrase = passphrase
    
    def encrypt_file(self, input_path, output_path=None):
        """Encrypt a file and save to output path"""
        input_file = Path(input_path)
        
        if not input_file.exists():
            print(f"Error: File {input_path} not found")
            return False
        
        if not self._is_supported_format(input_file.suffix):
            print(f"Warning: File format {input_file.suffix} may not be optimized")
        
        if output_path is None:
            output_path = str(input_file) + '.encrypted'
        
        try:
            # Read file content
            with open(input_file, 'rb') as f:
                file_data = f.read()
            
            # Generate key from passphrase
            key = self.engine.generate_key(self.passphrase)
            
            # Encrypt data
            encrypted_data = self.engine.encrypt_aes256(file_data, key)
            
            # Write encrypted file
            with open(output_path, 'wb') as f:
                f.write(encrypted_data)
            
            print(f"✓ File encrypted successfully: {output_path}")
            return True
        except Exception as e:
            print(f"Error encrypting file: {e}")
            return False
    
    def decrypt_file(self, input_path, output_path=None):
        """Decrypt an encrypted file and save to output path"""
        input_file = Path(input_path)
        
        if not input_file.exists():
            print(f"Error: File {input_path} not found")
            return False
        
        if output_path is None:
            output_path = str(input_file).replace('.encrypted', '_decrypted')
        
        try:
            # Read encrypted file
            with open(input_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Generate key from passphrase
            key = self.engine.generate_key(self.passphrase)
            
            # Decrypt data
            decrypted_data = self.engine.decrypt_aes256(encrypted_data, key)
            
            # Write decrypted file
            with open(output_path, 'wb') as f:
                f.write(decrypted_data)
            
            print(f"✓ File decrypted successfully: {output_path}")
            return True
        except Exception as e:
            print(f"Error decrypting file: {e}")
            return False
    
    def _is_supported_format(self, file_extension):
        """Check if file format is in supported list"""
        return file_extension.lower() in self.SUPPORTED_FORMATS
    
    def batch_encrypt(self, directory, pattern='*'):
        """Encrypt all files matching pattern in directory"""
        dir_path = Path(directory)
        count = 0
        
        for file in dir_path.glob(pattern):
            if file.is_file():
                if self.encrypt_file(str(file)):
                    count += 1
        
        print(f"\nEncrypted {count} files")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: encrypt_file.py <encrypt|decrypt> <file> [passphrase]")
        sys.exit(1)
    
    command = sys.argv[1]
    file_path = sys.argv[2]
    passphrase = sys.argv[3] if len(sys.argv) > 3 else "DefaultPassword"
    
    encryptor = FileEncryptor(passphrase)
    
    if command == 'encrypt':
        encryptor.encrypt_file(file_path)
    elif command == 'decrypt':
        encryptor.decrypt_file(file_path)
    else:
        print(f"Unknown command: {command}")

# Written by: AI Agents
# License: MIT
