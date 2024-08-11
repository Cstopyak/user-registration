from passlib.context import CryptContext
from app.models import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
#allows us to hash plain text passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def addUser(
        session:Session,
        username:str,
        email:str,
        password:str
) -> User | None:
    hashedPassword = pwd_context.hash(password)
    dbUser = User(username=username, email=email, password=hashedPassword)
    session.add(dbUser)
    try:
        session.commit()
        session.refresh(dbUser)
        return dbUser
    except IntegrityError:
        session.rollback()
        return None