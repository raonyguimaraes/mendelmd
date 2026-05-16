import anthropic
from individuals.models import Individual
from django.utils.text import slugify
from django.conf import settings
import os
import json


def _get_claude_history(messages):
    history = []
    for msg in messages:
        if msg.role in ('user', 'assistant'):
            history.append({'role': msg.role, 'content': msg.content})
    return history


def run_claude(user_message, conversation):
    client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
    history = _get_claude_history(list(conversation.messages.all()))
    # Remove the last user message — it's already in history; we'll pass it fresh
    if history and history[-1]['role'] == 'user':
        history = history[:-1]

    response = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=2048,
        system=(
            'You are an AI assistant integrated into Rockbio (MendelMD), a genomics platform for '
            'analyzing NGS data and identifying disease-causing variants. '
            'You help researchers with variant analysis, bioinformatics questions, and platform usage. '
            'Be concise and accurate.'
        ),
        messages=history + [{'role': 'user', 'content': user_message}],
    )
    return response.content[0].text


def run_annotation_agent(command, user):
    parts = command.strip().split()
    sub = parts[0].lower() if parts else ''

    if sub == 'list':
        individuals = Individual.objects.filter(user=user).order_by('-id')[:10]
        if not individuals:
            return 'No individuals found.'
        lines = ['Recent individuals:']
        for ind in individuals:
            lines.append(f'  #{ind.id} {ind.name} — status: {ind.status}')
        return '\n'.join(lines)

    if sub == 'status' and len(parts) >= 2:
        try:
            ind_id = int(parts[1])
            ind = Individual.objects.get(pk=ind_id, user=user)
        except (ValueError, Individual.DoesNotExist):
            return f'Individual #{parts[1]} not found.'
        username = slugify(ind.user.username)
        progress_path = os.path.join(settings.BASE_DIR, 'genomes', username, str(ind.id), 'annotation.progress.json')
        progress = {}
        if os.path.exists(progress_path):
            try:
                with open(progress_path) as f:
                    progress = json.load(f)
            except ValueError:
                pass
        stage = progress.get('stage') or ind.status
        percent = progress.get('percent', 0) or 0
        message = progress.get('message', '')
        return (
            f'Individual #{ind.id} — {ind.name}\n'
            f'  Status : {ind.status}\n'
            f'  Stage  : {stage}\n'
            f'  Percent: {percent}%\n'
            f'  Message: {message}'
        )

    return (
        'Annotation agent commands:\n'
        '  /annotate list             — list your recent individuals\n'
        '  /annotate status <id>      — get annotation progress for an individual'
    )


def run_custom_agent(command):
    return f'Custom agent received: {command}\n(Wire up your own logic in chat/agents.py → run_custom_agent)'


def dispatch(user_message, conversation, user):
    msg = user_message.strip()

    if msg.startswith('/annotate'):
        return 'annotation', run_annotation_agent(msg[len('/annotate'):].strip(), user)

    if msg.startswith('/custom'):
        return 'custom', run_custom_agent(msg[len('/custom'):].strip())

    if msg.startswith('/help'):
        return 'claude', (
            'Available commands:\n'
            '  /annotate list           — list your individuals\n'
            '  /annotate status <id>    — annotation progress\n'
            '  /custom <cmd>            — custom agent\n'
            '  /help                    — show this help\n'
            'Anything else goes to Claude.'
        )

    return 'claude', run_claude(msg, conversation)
