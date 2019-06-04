from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Boolean
class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    
    alt = Column(Integer)

    questionText = Column(String(length=100))
    correctAnswer = Column(String(length=100))