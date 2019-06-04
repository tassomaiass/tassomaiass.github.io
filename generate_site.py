from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Question

engine = create_engine("sqlite:///tassomaiass.db")
Session = sessionmaker(bind=engine)


def markdown_sanitize(text):
    markdownspecials = "\\`*_{}[]()#+-.!"

    sanitized = ""
    for c in text:
        if c in markdownspecials:
            sanitized += "\\"
        sanitized += c
    
    return sanitized

def sanitize(text):
    sanitized = text.replace('\n', ' ')
    sanitized = markdown_sanitize(sanitized)

    return sanitized

def main():
    with open('base.md', 'r') as file:
        base_md = file.read()

    processed_questions = []
    qna = [] # [["Question", "Answer", "Answer", ..]]

    db = Session()
    questions = db.query(Question).all()

    for question in questions:
        for i, processed_question in enumerate(processed_questions):
            if processed_question == question.questionText:
                qna[i].append(question.correctAnswer)
                break
        else:
            processed_questions.append(question.questionText)
            qna.append([question.questionText, question.correctAnswer])
        
    
    final = base_md

    for q in qna:
        question = q.pop(0)
        final += "#### " + sanitize(question) + "\n"
        for answer in q:
            final += "* " + sanitize(answer) + "\n"
        final += "\n"
    
    with open('answers.md', 'w') as file:
        file.write(final)
        file.truncate()


if __name__ == "__main__":
    main()