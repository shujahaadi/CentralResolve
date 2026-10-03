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

IMPORTANT RULES:

1. Never use null.
2. Never invent information.
3. person must be extracted from the message when a person is mentioned.
4. task must describe the actual task or subject.
5. source_message must contain the COMPLETE original message, not just the person's name.
6. Preserve the original meaning.
7. If a fact does not clearly contain a person or task, use an empty string "".
8. Extract multiple facts when multiple messages contain facts.

Example:

Input:
Rahul: I'll handle deployment.
Ahmed: Frontend will be done Sunday.
Sana: The presentation deadline is Monday.

Output:
{
  "facts": [
    {
      "type": "task_assignment",
      "person": "Rahul",
      "task": "deployment",
      "value": "Rahul will handle deployment",
      "source_message": "Rahul: I'll handle deployment."
    },
    {
      "type": "deadline",
      "person": "Ahmed",
      "task": "frontend",
      "value": "Sunday",
      "source_message": "Ahmed: Frontend will be done Sunday."
    },
    {
      "type": "deadline",
      "person": "Sana",
      "task": "presentation",
      "value": "Monday",
      "source_message": "Sana: The presentation deadline is Monday."
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