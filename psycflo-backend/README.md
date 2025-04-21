 What's Inside

 Django + Django REST Framework project
   Apps included:
  users/ – User registration & login
  chatbot/ – AI-powered mental health chatbot
  aid/ – Menstrual aid request system
  therapy/ –  therapy session booking


##  How to Clone & Run the Project

bash
git clone https://github.com/Redieet/-psycflo-backend.git
cd -psycflo-backend
python -m venv venv
venv\Scripts\activate       # Use 'source venv/bin/activate' on Mac/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
