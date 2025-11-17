@dataclass
class JWTConfig:
    secret_key: str = os.getenv("JWT_SECRET_KEY", "default-secret")
    algorithm: str = "HS256"
    expire_minutes: int = 60
