# Django Polls App

A simple polling app where users can vote on questions.

## How to Run

1. Install Django
```bash
pip install django
2. Run the server
python manage.py runserver
3. Go to http://127.0.0.1:8000/polls/
Pages
- /polls/ - See all questions
- /polls/1/ - Vote on a question
- /polls/1/results/ - See results
- /admin/ - Manage questions (create superuser first)
Create Admin User
python manage.py createsuperuser
Run Tests
python manage.py test polls
