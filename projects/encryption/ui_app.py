#!/usr/bin/env python3
"""
Encryption UI Application
Gtkinter-based GUI for encryption/decryption
AI-Generated Implementation with Red and Black Theme
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from encrypt_file import FileEncryptor
import os

class EncryptionApp:
    """Tkinter GUI for encryption/decryption"""
    
    # Red and Black Theme
    DARK_BG = "#1a1a1a"
    RED_ACCENT = "#e74c3c"
    BLACK_ACCENT = "#0f0f0f"
    TEXT_COLOR = "#ffffff"
    
    def __init__(self, root):
        self.root = root
        self.root.title("AES-256 Encryption Tool")
        self.root.geometry("600x500")
        self.root.configure(bg=self.DARK_BG)
        self.setup_styles()
        self.setup_ui()
    
    def setup_styles(self):
        """Configure application styles"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background=self.DARK_BG, foreground=self.TEXT_COLOR)
        style.configure('Title.TLabel', background=self.DARK_BG, foreground=self.RED_ACCENT,
                       font=('Arial', 14, 'bold'))
        style.configure('TButton', background=self.RED_ACCENT, foreground=self.TEXT_COLOR)
        style.configure('TEntry', fieldbackground=self.BLACK_ACCENT, foreground=self.TEXT_COLOR)
    
    def setup_ui(self):
        """Build user interface"""
        # Title
        title = ttk.Label(self.root, text="AES-256 Encryption Suite", style='Title.TLabel')
        title.pack(pady=20)
        
        # File selection frame
        file_frame = tk.Frame(self.root, bg=self.DARK_BG)
        file_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(file_frame, text="Select File:").pack(anchor='w')
        self.file_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path, width=40).pack(fill='x', pady=5)
        ttk.Button(file_frame, text="Browse...", command=self.browse_file).pack(anchor='w')
        
        # Passphrase frame
        pass_frame = tk.Frame(self.root, bg=self.DARK_BG)
        pass_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(pass_frame, text="Passphrase:").pack(anchor='w')
        self.passphrase = tk.StringVar()
        ttk.Entry(pass_frame, textvariable=self.passphrase, show="*", width=40).pack(fill='x', pady=5)
        
        # Action buttons frame
        button_frame = tk.Frame(self.root, bg=self.DARK_BG)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Encrypt", command=self.encrypt_file).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Decrypt", command=self.decrypt_file).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side='left', padx=10)
        
        # Status frame
        status_frame = tk.Frame(self.root, bg=self.DARK_BG)
        status_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        ttk.Label(status_frame, text="Status:").pack(anchor='w')
        self.status_text = tk.Text(status_frame, height=8, bg=self.BLACK_ACCENT, 
                                   fg=self.TEXT_COLOR, insertbackground=self.RED_ACCENT)
        self.status_text.pack(fill='both', expand=True, pady=5)
        
        # Info label
        info = ttk.Label(self.root, text="Red & Black Theme | 256-bit Encryption | AI-Generated",
                        style='TLabel')
        info.pack(pady=10)
    
    def browse_file(self):
        """Open file browser dialog"""
        filename = filedialog.askopenfilename()
        if filename:
            self.file_path.set(filename)
            self.log(f"Selected: {os.path.basename(filename)}")
    
    def encrypt_file(self):
        """Encrypt selected file"""
        if not self.file_path.get() or not self.passphrase.get():
            messagebox.showerror("Error", "Please select a file and enter a passphrase")
            return
        
        try:
            encryptor = FileEncryptor(self.passphrase.get())
            if encryptor.encrypt_file(self.file_path.get()):
                self.log("✓ Encryption completed successfully")
                messagebox.showinfo("Success", "File encrypted successfully")
            else:
                self.log("✗ Encryption failed")
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Encryption failed: {e}")
    
    def decrypt_file(self):
        """Decrypt selected file"""
        if not self.file_path.get() or not self.passphrase.get():
            messagebox.showerror("Error", "Please select a file and enter a passphrase")
            return
        
        try:
            encryptor = FileEncryptor(self.passphrase.get())
            if encryptor.decrypt_file(self.file_path.get()):
                self.log("✓ Decryption completed successfully")
                messagebox.showinfo("Success", "File decrypted successfully")
            else:
                self.log("✗ Decryption failed")
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Decryption failed: {e}")
    
    def clear_fields(self):
        """Clear all fields"""
        self.file_path.set("")
        self.passphrase.set("")
        self.status_text.delete(1.0, tk.END)
        self.log("Fields cleared")
    
    def log(self, message):
        """Add message to status log"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()

# Written by: AI Agents
# License: MIT
