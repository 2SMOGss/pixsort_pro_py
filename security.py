import hashlib, getpass, secrets, string
class VaultSecurity:
    def __init__(self, vault_dir):
        self.pwd_file = vault_dir / ".vault_key"
        self.recovery_file = vault_dir / ".recovery_key"
    def setup(self):
        if not self.pwd_file.exists():
            print("\n[FIRST-TIME SETUP] Security Initialization...")
            pwd = getpass.getpass("Create Master Vault Password: ")
            recovery = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            with open(self.pwd_file, "w") as f: f.write(hashlib.sha256(pwd.encode()).hexdigest())
            with open(self.recovery_file, "w") as f: f.write(hashlib.sha256(recovery.encode()).hexdigest())
            print(f"\n[IMPORTANT] RECOVERY KEY: {recovery}\nSave this now!")
            input("Press Enter to proceed...")
    def verify(self):
        attempt = getpass.getpass("\n[SECURITY] Vault Access Required: ")
        hashed_attempt = hashlib.sha256(attempt.encode()).hexdigest()
        with open(self.pwd_file, "r") as f: return hashed_attempt == f.read().strip()
