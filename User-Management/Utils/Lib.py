from cryptography.fernet import Fernet,InvalidToken


class Libraries:
    
   
    # Generate a key
    @staticmethod
    def generate_key():
        key = Fernet.generate_key()
        return key

    # Encrypt data
    @staticmethod
    def encrypt_data(data):
        SECRET_KEY = b'4G-L8utlxR2BWU8Yz9FyLy2c2H5m7M_rT8a9sQx35Hs='
        fernet = Fernet(SECRET_KEY)
        encrypted = fernet.encrypt(data.encode())  # Encoding data to bytes
        return encrypted

    # Decrypt data
    @staticmethod 
    def decrypt_data(encrypted_data):
        SECRET_KEY = b'4G-L8utlxR2BWU8Yz9FyLy2c2H5m7M_rT8a9sQx35Hs='
        fernet = Fernet(SECRET_KEY)
        try:
            return fernet.decrypt(encrypted_data).decode()  # Ensure you're decrypting bytes
        except InvalidToken:
            return "Invalid token or data has changed"  # Provide some feedback if necessary