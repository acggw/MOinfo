from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from .base import Base
from werkzeug.security import check_password_hash, generate_password_hash
from config.errors import Errors

class User(Base):
    __tablename__ = "users"

    username = mapped_column(String, primary_key=True, nullable=False)
    password_hash = mapped_column(String)

    notifications_sent = relationship("Notification", back_populates="sent_to")

    preferences = relationship("User_Preference", back_populates="user")

    email = mapped_column(String, unique=True)
    email_notifications = mapped_column(Integer)

    phone = mapped_column(String, unique=True)
    phone_notifications = mapped_column(Integer)

    verified = mapped_column(String)

    admin = mapped_column(String)

def create_user(session, user_name, password, email, email_nots, phone, phone_nots):
    if(session.get(User, (user_name)) != None):
        raise Errors.DUPLICATE_USER_NAME_ERROR
    if(session.query(User).filter(User.email == email).first()):
        raise Errors.DUPLICATE_EMAIL_ERROR
    if(session.query(User).filter(User.phone == phone).first()):
        raise Errors.DUPLICATE_PHONE_ERROR
    
    user = User(
        username = user_name,
        password_hash = generate_password_hash(password),
        email = email,
        email_notifications = email_nots,
        phone = phone,
        phone_notifications = phone_nots,
        verified = "N/A",
        admin = "No"
    )

    session.add(user)
    session.commit()

def create_admin(session, user_name, password, email, phone):
    if(session.get(User, (user_name)) != None):
        raise Errors.DUPLICATE_USER_NAME_ERROR
    if(session.query(User).filter(User.email == email).first()):
        raise Errors.DUPLICATE_EMAIL_ERROR
    if(session.query(User).filter(User.phone == phone).first()):
        raise Errors.DUPLICATE_PHONE_ERROR
    
    user = User(
        username = user_name,
        password_hash = generate_password_hash(password),
        email = email,
        phone = phone,
        verified = "N/A",
        admin = "Yes"
    )

    session.add(user)
    session.commit()

def verify_user(session, user_name, password_hash):
    user = session.get(User, (user_name))
    if(user == None):
        return False
    if(check_password_hash(user.password_hash, password_hash)):
        return True
    
def user_exists(session, user_name):
    user = session.get(User, (user_name))
    if(user == None):
        return False
    else:
        return True

class User_Preference(Base):
    __tablename__ = "user_preferences"

    username = mapped_column(Integer, ForeignKey("users.username"), primary_key=True)
    policy_area = mapped_column(String, primary_key=True)
    importance_threshold = mapped_column(Integer)

    user = relationship("User", back_populates="preferences")

def set_preference(session, username, policy_area, importance):
    if(not user_exists(session, username)):
        raise Errors.USER_NOT_FOUND_ERROR
    
    pref = session.get(User_Preference, (username, policy_area))

    importance_threshold = 0
    if(type(importance) == str):
        if importance == "interest_low":
            importance_threshold = 1
        elif importance == "interest_medium":
            importance_threshold = 2
        elif importance == "interest_high":
            importance_threshold = 3

    if(pref == None):
        session.add(User_Preference(
            username = username,
            policy_area = policy_area,
            importance_threshold = importance_threshold,
            user = session.get(User, (username))
        ))
    else:
        setattr(pref, "importance_threshold", importance_threshold)

    session.commit()

def preference_exists(session, username, policy_area):
    if(not verify_user(session, username)):
        raise Errors.USER_NOT_FOUND_ERROR
    if session.get(User_Preference, (username, policy_area)):
        return True
    return False

def get_preference(session, username, policy_area):
    if(not verify_user(session, username)):
        raise Errors.USER_NOT_FOUND_ERROR
    return session.get(User_Preference, (username, policy_area))

def get_preferences(session, username):
    if(not verify_user(session, username)):
        raise Errors.USER_NOT_FOUND_ERROR
    return session.get(User, username).preferences




