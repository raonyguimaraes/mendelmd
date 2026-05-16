from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Conversation, Message
from .agents import dispatch


@login_required
def index(request):
    conversations = Conversation.objects.filter(user=request.user)
    # Auto-create a conversation on first visit
    if not conversations.exists():
        conv = Conversation.objects.create(user=request.user)
    else:
        conv = conversations.first()
    return redirect('chat_conversation', conversation_id=conv.id)


@login_required
def conversation(request, conversation_id):
    conv = get_object_or_404(Conversation, pk=conversation_id, user=request.user)
    conversations = Conversation.objects.filter(user=request.user)
    return render(request, 'chat/chat.html', {
        'conversation': conv,
        'conversations': conversations,
        'messages': conv.messages.all(),
    })


@login_required
@require_POST
def new_conversation(request):
    conv = Conversation.objects.create(user=request.user, title='New conversation')
    return redirect('chat_conversation', conversation_id=conv.id)


@login_required
@require_POST
def send_message(request, conversation_id):
    conv = get_object_or_404(Conversation, pk=conversation_id, user=request.user)
    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'error': 'empty'}, status=400)

    Message.objects.create(conversation=conv, role='user', agent='claude', content=content)

    try:
        agent, reply = dispatch(content, conv, request.user)
        msg = Message.objects.create(conversation=conv, role='assistant', agent=agent, content=reply)
        # Update conversation title from first user message
        if conv.messages.filter(role='user').count() == 1:
            conv.title = content[:60]
            conv.save()
        return JsonResponse({'message': msg.to_dict()})
    except Exception as e:
        error_msg = f'Agent error: {e}'
        msg = Message.objects.create(conversation=conv, role='system', agent='claude', content=error_msg)
        return JsonResponse({'message': msg.to_dict()})


@login_required
def poll_messages(request, conversation_id):
    conv = get_object_or_404(Conversation, pk=conversation_id, user=request.user)
    since_id = int(request.GET.get('since', 0))
    msgs = conv.messages.filter(id__gt=since_id)
    return JsonResponse({'messages': [m.to_dict() for m in msgs]})
