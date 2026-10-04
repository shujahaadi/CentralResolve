from app.schemas.analysis import ProjectFact
from app.schemas.conflict import Conflict, Conflicts, ConflictEvidence


def normalize_deadline(value: str) -> str:
    return value.lower().strip()


def detect_conflicts(facts: list[ProjectFact]) -> Conflicts:
    conflicts = []

    deadlines = {}
    assignments = {}
    statuses = {}

    for fact in facts:
        if fact.type == "task_assignment":
            key = fact.task.lower().strip()
            assignments.setdefault(key, []).append(fact)

        elif fact.type == "deadline":
            key = fact.task.lower().strip()
            deadlines.setdefault(key, []).append(fact)

        elif fact.type == "status":
            key = fact.task.lower().strip()
            statuses.setdefault(key, []).append(fact)

    # Ownership conflicts
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
                            ConflictEvidence(
                                platform=fact.platform,
                                message=fact.source_message,
                            )
                            for fact in person_facts
                        ],
                    )
                )

    # Deadline conflicts
    for task, task_facts in deadlines.items():
        normalized_values = {}

        for fact in task_facts:
            deadline = normalize_deadline(fact.value)
            normalized_values.setdefault(deadline, []).append(fact)

        if len(normalized_values) > 1:
            evidence = [
                ConflictEvidence(
                    platform=fact.platform,
                    message=fact.source_message,
                )
                for fact in task_facts
            ]

            conflicts.append(
                Conflict(
                    type="deadline_conflict",
                    task=task,
                    description=(
                        f"Different deadlines were stated for {task}: "
                        f"{', '.join(normalized_values.keys())}."
                    ),
                    severity="high",
                    evidence=evidence,
                )
            )

    # Status conflicts
    incompatible_statuses = [
        {"blocked", "completed"},
        {"blocked", "done"},
        {"not started", "completed"},
        {"not started", "done"},
        {"cancelled", "active"},
        {"cancelled", "in progress"},
    ]

    for task, task_facts in statuses.items():
        normalized_statuses = {}

        for fact in task_facts:
            status = fact.value.lower().strip()
            normalized_statuses.setdefault(status, []).append(fact)

        status_values = set(normalized_statuses.keys())

        conflict_found = any(
            pair.issubset(status_values)
            for pair in incompatible_statuses
        )

        if conflict_found:
            conflicts.append(
                Conflict(
                    type="status_conflict",
                    task=task,
                    description=(
                        f"Incompatible statuses were reported for {task}: "
                        f"{', '.join(status_values)}."
                    ),
                    severity="medium",
                    evidence=[
                        ConflictEvidence(
                            platform=fact.platform,
                            message=fact.source_message,
                        )
                        for fact in task_facts
                    ],
                )
            )

    # Unresolved decisions
    unresolved = {}

    for fact in facts:
        if fact.type != "unresolved":
            continue

        key = fact.task.lower().strip()
        unresolved.setdefault(key, []).append(fact)

    for task, task_facts in unresolved.items():
        conflicts.append(
            Conflict(
                type="unresolved_decision",
                task=task,
                description=(
                    f"The decision about {task} is still unresolved."
                ),
                severity="medium",
                evidence=[
                    ConflictEvidence(
                        platform=fact.platform,
                        message=fact.source_message,
                    )
                    for fact in task_facts
                ],
            )
        )

    return Conflicts(conflicts=conflicts)