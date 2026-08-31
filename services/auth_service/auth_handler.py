import hashlib, hmac, time
from shared.models import User

class AuthService:
    def __init__(self, secret_key: str = 'dev-secret-12345'):
        self.secret_key = secret_key.encode('utf-8')
        self.user_store = {}

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8') + self.secret_key).hexdigest()

    def register(self, user_id: str, email: str, password: str) -> User:
        pw_hash = self.hash_password(password)
        user = User(id=user_id, email=email, password_hash=pw_hash)
        self.user_store[user_id] = user
        return user

    def generate_token(self, user: User, expires_in_sec: int = 3600) -> str:
        payload = f"{user.id}:{user.role}:{time.time() + expires_in_sec}"
        sig = hmac.new(self.secret_key, payload.encode('utf-8'), hashlib.sha256).hexdigest()
        return f"{payload}.{sig}"

    def verify_token(self, token: str) -> bool:
        parts = token.rsplit('.', 1)
        if len(parts) != 2:
            return False
        payload, sig = parts
        expected_sig = hmac.new(self.secret_key, payload.encode('utf-8'), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return False
        user_id, role, expiry = payload.split(':')
        return time.time() < float(expiry)

# CodeNomad Session [auth-jwt-refresh]: Refresh Token Rotation and Revocation

    def refresh_token(self, user_id: str) -> str:
        import time
        return f'refresh_{user_id}_{time.time()}'
