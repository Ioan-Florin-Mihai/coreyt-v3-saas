import hashlib
import hmac
import secrets


class ApiKeyManager:
    """Production-grade API key generation and hashing."""

    KEY_PREFIX = "sk"
    KEY_LENGTH = 32
    DISPLAY_PREFIX_LENGTH = 8

    @staticmethod
    def generate_key() -> str:
        """Generate secure API key."""
        random_bytes = secrets.token_bytes(ApiKeyManager.KEY_LENGTH)
        random_hex = random_bytes.hex()
        return f"{ApiKeyManager.KEY_PREFIX}_{random_hex}"

    @staticmethod
    def hash_key(key: str) -> str:
        """Hash API key using SHA-256."""
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    @staticmethod
    def extract_prefix(key: str) -> str:
        """Extract prefix for fast lookup."""
        try:
            return key.split("_")[1][: ApiKeyManager.DISPLAY_PREFIX_LENGTH]
        except IndexError:
            return ""

    @staticmethod
    def verify_key(incoming_key: str, stored_hash: str) -> bool:
        """Constant-time verification."""
        incoming_hash = ApiKeyManager.hash_key(incoming_key)
        return hmac.compare_digest(incoming_hash, stored_hash)