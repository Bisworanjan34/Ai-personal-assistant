from django.shortcuts import redirect, render
from groq import APIConnectionError
from .services import ai_response
from .models import Conversation, Message
from django.contrib.auth.decorators import login_required


# def ask_ai(request, conversation_id=None):
#     # 1. Always ensure a conversation exists
#     all_conversations = Conversation.objects.filter(user=request.user).order_by("-id")

#     # 2. Get the specific conversation requested (or the latest one)
#     if conversation_id:
#         conversation = Conversation.objects.get(id=conversation_id, user=request.user)
#     else:
#         conversation = all_conversations.first() or Conversation.objects.create(
#             user=request.user, title="new conversation"
#         )
#     # 2. Handle incoming messages
#     if request.method == "POST":
#         query = request.POST.get("query")

#         # 3. Rename ONLY if it is still the default "new conversation"
#         if conversation.title.strip().lower() == "new conversation":
#             conversation.title = query[:50]
#             conversation.save()
#         # 4. Save message and get AI response
#         Message.objects.create(conversation=conversation, role="user", content=query)

#         db_sms = conversation.messages.all().order_by("created")
#         ai_context = [{"role": sms.role, "content": sms.content} for sms in db_sms]
#         answer = ai_response(ai_context)

#         Message.objects.create(
#             conversation=conversation, role="assistant", content=answer
#         )
#         return redirect("aiapp:ask_ai")

#     # 5. Render page
#     messages = conversation.messages.all().order_by("created")
#     return render(
#         request,
#         "aiapp/ask_ai.html",
#         {
#             "conv": conversation,
#             "history": messages,
#             "all_conversations": all_conversations,  # Pass this!
#         },
#     )


@login_required(login_url="core:login")
def ask_ai(request, conversation_id=None):
    all_conversation = Conversation.objects.filter(user=request.user).order_by("-id")
    if conversation_id:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
    else:
        conversation = all_conversation.first() or Conversation.objects.create(
            user=request.user, title="new conversation"
        )
    if request.method == "POST":
        query = request.POST.get("query")
        if conversation.title.strip().lower() == "new conversation":
            conversation.title = query[:50]
            conversation.save()
        Message.objects.create(conversation=conversation, role="user", content=query)
        sms_db = conversation.messages.all().order_by("created")
        ai_context = [{"role": s.role, "content": s.content} for s in sms_db]
        try:
            answer = ai_response(ai_context)
        except APIConnectionError:
            answer = "i'am sorry to connect please try after some time"
        Message.objects.create(
            conversation=conversation, role="assistant", content=answer
        )
        return redirect("aiapp:ask_ai")
    messages = conversation.messages.all().order_by("created")
    context = {
        "history": messages,
        "all_conversations": all_conversation,
        "conv": conversation,
    }
    return render(request, "aiapp/ask_ai.html", context)


@login_required(login_url="core:login")
def new_chat(request):
    # This specifically creates a fresh start
    Conversation.objects.create(user=request.user, title="new conversation")
    return redirect("aiapp:ask_ai")
