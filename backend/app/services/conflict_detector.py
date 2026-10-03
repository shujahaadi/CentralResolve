from app.schemas.analysis import ProjectFact
from app.schemas.conflict import Conflict, Conflicts


def detect_conflicts(facts: list[ProjectFact]) -> Conflicts:
    conflicts = []

    assignments = {}

    for fact in facts:
        if fact.type != "task_assignment":
            continue

        key = fact.task.lower().strip()

        assignments.setdefault(key, []).append(fact)

    for task, task_facts in assignments.items():
        people = {}

        for fact in task_facts:
            people.setdefault(fact.person, []).append(fact)

        for person, person_facts in people.items():
            positive_assignment = any(
                "will handle" in fact.value.lower()
                or "will take" in fact.value.lower()
                or "assigned" in fact.value.lower()
                for fact in person_facts
            )

            withdrawal = any(
                "can't handle" in fact.value.lower()
                or "cannot handle" in fact.value.lower()
                or "can't take" in fact.value.lower()
                or "cannot take" in fact.value.lower()
                or "anymore" in fact.value.lower()
                for fact in person_facts
            )

            if positive_assignment and withdrawal:
                conflicts.append(
                    Conflict(
                        type="ownership_conflict",
                        task=task,
                        description=(
                            f"{person} was assigned to {task}, "
                            f"but later stated they could no longer handle it."
                        ),
                        severity="high",
                        evidence=[
                            fact.source_message
                            for fact in person_facts
                        ],
                    )
                )

    return Conflicts(conflicts=conflicts)