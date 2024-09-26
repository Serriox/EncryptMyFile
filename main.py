import customtkinter
import tkinter
import tkinter.messagebox
import cryptography
import cryptography.fernet
import pyperclip
import os

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("EncryptMyFile")

        self.iconbitmap("icon.ico")
        self.geometry("800x600")
        self.resizable(False, False)

        self.grid_columnconfigure(
            index = 1,
            weight = 1
        )
        self.grid_columnconfigure(
            index = (2, 3),
            weight = 0
        )
        self.grid_rowconfigure(
            index = (0, 1, 2),
            weight = 1
        )



        self.sidebar_frame = customtkinter.CTkFrame(
            master = self,
            height = 600,
            corner_radius = 0
        )
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.title_label = customtkinter.CTkLabel(
            master = self.sidebar_frame,
            text = "EncryptMyFile",
            font = customtkinter.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=24, pady=24)



        self.tabview = customtkinter.CTkTabview(
            master = self,
            width = 496,
            height = 256
        )
        self.tabview.grid(row=0, column=1, padx=32, pady=32, sticky="nsew")

        self.tabview.add("Encrypt")
        self.tabview.add("Decrypt")



        self.key_label = customtkinter.CTkLabel(
            master = self.tabview.tab("Encrypt"),
            text = "Encryption key",
            font = customtkinter.CTkFont(size=20)
        )
        self.key_label.grid(row=0, column=0, padx=8, pady=(32, 8))

        self.key_text = customtkinter.CTkEntry(
            master = self.tabview.tab("Encrypt"),
            width = 496,
            font = customtkinter.CTkFont(size=16)
        )
        self.key_text.insert("0", "Encryption key isn't generated yet...")
        self.key_text.configure(state="disabled")
        self.key_text.grid(row=1, column=0, padx=8, pady=8)

        self.generate_key_button = customtkinter.CTkButton(
            master = self.tabview.tab("Encrypt"),
            text = "Generate new key",
            font = customtkinter.CTkFont(size=16),
            command = self.generate_new_key
        )
        self.generate_key_button.grid(row=2, column=0, padx=8, pady=8)



        self.path_label = customtkinter.CTkLabel(
            master = self.tabview.tab("Encrypt"),
            text = "File paths",
            font = customtkinter.CTkFont(size=20)
        )
        self.path_label.grid(row=3, column=0, padx=8, pady=(32, 8))

        self.path_text = customtkinter.CTkEntry(
            master = self.tabview.tab("Encrypt"),
            width = 496,
            placeholder_text = "Insert path to file you want to encrypt",
            font = customtkinter.CTkFont(size=16)
        )
        self.path_text.grid(row=4, column=0, padx=8, pady=8)



        self.enc_path_text = customtkinter.CTkEntry(
            master = self.tabview.tab("Encrypt"),
            width = 496,
            placeholder_text = "Insert path where encrypted file should be created",
            font = customtkinter.CTkFont(size=16)
        )
        self.enc_path_text.grid(row=5, column=0, padx=8, pady=8)



        self.encrypt_button = customtkinter.CTkButton(
            master = self.tabview.tab("Encrypt"),
            text = "ENCRYPT",
            font = customtkinter.CTkFont(size=16),
            command = lambda: self.encrypt(self.path_text.get(), self.enc_path_text.get(), self.key_text.get())
        )
        self.encrypt_button.grid(row=6, column=0, padx=8, pady=(128, 8))





        self.key_label2 = customtkinter.CTkLabel(
            master = self.tabview.tab("Decrypt"),
            text = "Encryption Key",
            font = customtkinter.CTkFont(size=20)
        )
        self.key_label2.grid(row=0, column=0, padx=8, pady=(32, 8))

        self.key_text2 = customtkinter.CTkEntry(
            master = self.tabview.tab("Decrypt"),
            width = 496,
            placeholder_text = "Insert your encryption key",
            font = customtkinter.CTkFont(size=16)
        )
        self.key_text2.grid(row=1, column=0, padx=8, pady=8)



        self.path_label2 = customtkinter.CTkLabel(
            master = self.tabview.tab("Decrypt"),
            text = "File Paths",
            font = customtkinter.CTkFont(size=20)
        )
        self.path_label2.grid(row=2, column=0, padx=8, pady=(32, 8))

        self.path_text2 = customtkinter.CTkEntry(
            master = self.tabview.tab("Decrypt"),
            width = 496,
            placeholder_text = "Insert path to file you want to decrypt",
            font = customtkinter.CTkFont(size=16)
        )
        self.path_text2.grid(row=3, column=0, padx=8, pady=8)

        self.dec_path_text = customtkinter.CTkEntry(
            master = self.tabview.tab("Decrypt"),
            width = 496,
            placeholder_text = "Insert path where decrypted file should be created",
            font = customtkinter.CTkFont(size=16)
        )
        self.dec_path_text.grid(row=4, column=0, padx=8, pady=8)



        self.decrypt_button = customtkinter.CTkButton(
            master = self.tabview.tab("Decrypt"),
            text = "DECRYPT",
            font = customtkinter.CTkFont(size=16),
            command = lambda: self.decrypt(self.path_text2.get(), self.dec_path_text.get(), self.key_text2.get())
        )
        self.decrypt_button.grid(row=5, column=0, padx=8, pady=(128, 8))
    




    def generate_new_key(self):
        self.key = cryptography.fernet.Fernet.generate_key()

        self.key_text.configure(state="normal")
        self.key_text.delete("0", customtkinter.END)
        self.key_text.insert("0", self.key)
        self.key_text.configure(state="readonly")

        pyperclip.copy(self.key_text.get())

        tkinter.messagebox.showinfo(
            title = "Info",
            message = "Successfully generated new encryption key"
        )
    


    def encrypt(self, file_path, enc_file_path, key):
        self.file_data = None

        if key == "Encryption key isn't generated yet..." or file_path == "" or enc_file_path == "":
            if key == "The key isn't generated yet...":
                tkinter.messagebox.showerror(
                    title = "Error",
                    message = "Encryption key shouldn't be empty"
                )

            if file_path == "" or enc_file_path == "":
                tkinter.messagebox.showerror(
                    title = "Error",
                    message = "File path shouldn't be empty"
                )

            return

        try:
            with open(rf"{file_path}", "rb") as file:
                self.file_data = file.read()
            
            try:
                self.encrypted = cryptography.fernet.Fernet(key).encrypt(self.file_data)

                with open(rf"{enc_file_path}", "wb") as encrypted_file:
                    encrypted_file.write(self.encrypted)
                
                tkinter.messagebox.showinfo(
                    title = "Info",
                    message = f"Successfully encrypted your file\n\nOriginal file at \"{os.path.abspath(file_path)}\"\n\nEncrypted file at \"{os.path.abspath(enc_file_path)}\""
                )
            except:
                tkinter.messagebox.showerror(
                    title = "Error",
                    message = "Invalid encryption key"
                )

                return
        except FileNotFoundError:
            tkinter.messagebox.showerror(
                title = "Error",
                message = "File not found"
            )

            return

    def decrypt(self, file_path, dec_file_path, key):
        self.file_data = None

        if key == "" or file_path == "" or dec_file_path == "":
            if key == "":
                tkinter.messagebox.showerror(
                    title = "Error",
                    message = "Encryption key shouldn't be empty"
                )

            if file_path == "" or dec_file_path == "":
                tkinter.messagebox.showerror(
                    title = "Error",
                    message = "File path shouldn't be empty"
                )
            
            return
        
        try:
            with open(rf"{file_path}", "rb") as file:
                self.file_data = file.read()
            
            try:
                self.decrypted = cryptography.fernet.Fernet(key).decrypt(self.file_data)

                with open(rf"{dec_file_path}", "wb") as decrypted_file:
                    decrypted_file.write(self.decrypted)
                
                tkinter.messagebox.showinfo(
                    title = "Info",
                    message = f"Successfully decrypted your file\n\nOriginal file at \"{os.path.abspath(file_path)}\"\n\nDecrypted file at \"{os.path.abspath(dec_file_path)}\""
                )
            except:
                tkinter.messagebox.showerror(
                    title = "Error",
                    message = "Invalid encryption key"
                )

                return
        except FileNotFoundError:
            tkinter.messagebox.showerror(
                title = "Error",
                message = "File not found"
            )

            return

if __name__ == "__main__":
    app = App()
    app.mainloop()
