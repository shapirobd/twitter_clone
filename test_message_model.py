from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows, bcrypt
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

# Does basic model work?
# Does user_id correspond to the correct / signed in user?
# Does the user relationship function correctly?
# Does user.messages function correctly?
