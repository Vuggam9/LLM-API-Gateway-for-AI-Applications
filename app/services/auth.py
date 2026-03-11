from fastapi import Header, HTTPException, status

from app.core.config import get_settings



def require_api_key(x_api_key: str | None = Header(default=None)) -> str:
    settings = get_settings()
    if x_api_key is None or x_api_key not in settings.api_key_list:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
    return x_api_key
