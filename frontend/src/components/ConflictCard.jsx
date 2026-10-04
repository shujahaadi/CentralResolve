function ConflictCard({ conflict }) {
  const severityClass = conflict.severity.toLowerCase();

  const conflictTitles = {
    ownership_conflict: "Ownership Conflict",
    deadline_conflict: "Deadline Conflict",
    status_conflict: "Status Conflict",
    unresolved_decision: "Unresolved Decision",
  };

  const title =
    conflictTitles[conflict.type] || "Conflict Detected";

  return (
    <div className={`conflict-card ${severityClass}`}>
      <div className="conflict-header">
        <div>
          <span className="conflict-type">
            {title}
          </span>

          <h3>{conflict.task}</h3>
        </div>

        <span className={`severity ${severityClass}`}>
          {conflict.severity}
        </span>
      </div>

      <p className="conflict-description">
        {conflict.description}
      </p>

      <div className="evidence">
        <span className="evidence-label">
          EVIDENCE
        </span>

        {conflict.evidence.map((item, index) => (
          <div className="evidence-message" key={index}>
            <div className="evidence-platform">
              {item.platform}
            </div>

            <div className="evidence-content">
              <span className="evidence-mark">"</span>
              <span>{item.message}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ConflictCard;