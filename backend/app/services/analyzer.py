import json

from ollama import chat

from app.schemas.analysis import ProjectFacts


def analyze_messages(messages: str) -> ProjectFacts:
    response = chat(
        model="gemma3:4b",
        messages=[
            {
                "role": "system",
                "content": """
You are CentralResolve, a project conversation analysis system.

Analyze the conversation and extract concrete project facts.

For EVERY fact, return:

- type: one of task_assignment, deadline, status, decision, unresolved
- person: the person explicitly associated with the fact
- task: the task, work item, or subject associated with the fact
- value: the actual information being stated
- source_message: the COMPLETE original message that contains the fact
- platform: exactly "whatsapp" or "discord", copied from the [whatsapp] or [discord] prefix on the message

IMPORTANT RULES:

1. Never use null.
2. Never invent information.
3. person must be extracted from the message when a person is mentioned.
4. task must describe the actual task or subject.
5. source_message must contain the COMPLETE original message, not just the person's name.
6. Preserve the original meaning.
7. If a fact does not clearly contain a person or task, use an empty string "".
8. Extract multiple facts when multiple messages contain facts.
9. Never infer the platform. Always use the platform tag provided in the message.

Example:

Input:
[whatsapp] Rahul: I'll handle deployment.
[whatsapp] Ahmed: Frontend will be done Sunday.
[whatsapp] Sana: The presentation deadline is Monday.
[discord] Rahul: I can't handle deployment anymore.
[discord] Ahmed: Frontend is basically done.
[discord] Sana: I thought the presentation was due Friday.

Output:
{
  "facts": [
    {
      "type": "task_assignment",
      "platform": "whatsapp",
      "person": "Rahul",
      "task": "deployment",
      "value": "Rahul will handle deployment",
      "source_message": "Rahul: I'll handle deployment."
    },
    {
      "type": "deadline",
      "platform": "whatsapp",
      "person": "Ahmed",
      "task": "frontend",
      "value": "Sunday",
      "source_message": "Ahmed: Frontend will be done Sunday."
    }
  ]
}

Return ONLY valid JSON.
""",
            },
            {
                "role": "user",
                "content": messages,
            },
        ],
        format=ProjectFacts.model_json_schema(),
    )

    data = json.loads(response.message.content)

    return ProjectFacts.model_validate(data)