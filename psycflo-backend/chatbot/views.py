import openai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
@api_view(['POST'])
def chatbot_real(request):
    user_message = request.data.get("message")

    openai.api_key = settings.OPENAI_API_KEY

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful therapy chatbot."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion.choices[0].message["content"]
    except Exception as e:
        # fallback response for pushing/demo
        reply = "Sorry, I’m having trouble responding right now. Please try again later."

    return Response({"reply": reply})
