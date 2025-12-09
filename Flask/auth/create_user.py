from ...Scripts.session import Session
from ...Scripts.tables.user import User
from ...Scripts.errors import Errors
from werkzeug.security import generate_password_hash, check_password_hash

SALT = "woiugniewurbwo"

def create_user(user_name, password, email, phone):
    with Session as session:
        if(session.get(User, (user_name)) != None):
            raise Errors.DUPLICATE_USER_NAME_ERROR
        if(session.query(User).filter(User.email == email).first()):
            raise Errors.DUPLICATE_EMAIL_ERROR
        if(session.query(User).filter(User.phone == phone).first()):
            raise Errors.DUPLICATE_PHONE_ERROR
        
        user = User(
            username = user_name,
            password_hash = generate_password_hash(password + SALT),
            email = email,
            phone = phone
        )

        session.add(user)
        session.commit()
        
    