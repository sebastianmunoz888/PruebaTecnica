from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_password_hash
from app.core.config import settings


def init_db(db: Session) -> None:
    """Create initial user if it doesn't exist"""
    user = db.query(User).filter(User.email == settings.INITIAL_USER_EMAIL).first()
    
    if not user:
        user = User(
            email=settings.INITIAL_USER_EMAIL,
            hashed_password=get_password_hash(settings.INITIAL_USER_PASSWORD)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
       
    