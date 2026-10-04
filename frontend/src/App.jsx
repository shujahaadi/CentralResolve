import { useState } from "react";
import "./App.css";
import FileUpload from "./components/FileUpload";
import StatCard from "./components/StatCard";
import ConflictCard from "./components/ConflictCard";

function App() {
  const [whatsappFile, setWhatsappFile] = useState(null);
  const [discordFile, setDiscordFile] = useState(null);
  const [showUpload, setShowUpload] = useState(false);

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze() {
    if (!whatsappFile || !discordFile) {
      return;
    }

    setLoading(true);
    setError("");

    const formData = new FormData();

    formData.append("whatsapp_file", whatsappFile);
    formData.append("discord_file", discordFile);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/analyze",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed.");
      }

      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  if (results) {
    return (
      <div className="app">
        <nav className="navbar">
          <div className="logo">CentralResolve</div>

          <div className="results-nav">
            <span className="status">
              <span className="status-dot"></span>
              Analysis Complete
            </span>

            <button
              className="new-analysis-button"
              onClick={() => {
                setResults(null);
                setWhatsappFile(null);
                setDiscordFile(null);
                setError("");
                setShowUpload(true);
              }}
            >
              New Analysis
            </button>
          </div>
        </nav>

        <main className="results-page">
          <p className="eyebrow">ANALYSIS COMPLETE</p>

          <h2>Your team, in one picture.</h2>

          <div className="stats-grid">
            <StatCard
              label="WhatsApp Messages"
              value={results.whatsapp_messages}
            />

            <StatCard
              label="Discord Messages"
              value={results.discord_messages}
            />

            <StatCard
              label="Total Messages"
              value={results.total_messages}
            />

            <StatCard
              label="Conflicts"
              value={results.conflicts.length}
            />
          </div>

          <div className="analysis-summary">
              <div>
                <span className="summary-label">ATTENTION REQUIRED</span>
                <strong>{results.conflicts.length} conflicts need attention</strong>
              </div>

              <div className="summary-details">
                <span>
                  <strong>
                    {
                      results.conflicts.filter(
                        (conflict) => conflict.severity === "high"
                      ).length
                    }
                  </strong>
                  high severity
                </span>

                <span>
                  <strong>2</strong>
                  platforms
                </span>
              </div>
            </div>

          <section className="conflicts-section">
            <div className="section-heading">
              <div>
                <p className="eyebrow">WHAT NEEDS ATTENTION</p>
                <h3>Conflicts detected</h3>
              </div>

              <span className="conflict-count">
                {results.conflicts.length} found
              </span>
            </div>

            <div className="conflicts-list">
              {results.conflicts.map((conflict, index) => (
                <ConflictCard
                  key={index}
                  conflict={conflict}
                />
              ))}
            </div>
          </section>
        </main>
      </div>
    );
  }

  return (
    <div className="app">
      <nav className="navbar">
        <div className="logo">CentralResolve</div>

        <span className="status">
          <span className="status-dot"></span>
          Local Analysis
        </span>
      </nav>

      {!showUpload ? (
        <main className="hero">
          <div className="hero-content">
            <p className="eyebrow">
              CROSS-PLATFORM TEAM INTELLIGENCE
            </p>

            <h1>
              One project.
              <br />
              Multiple conversations.
              <br />
              <span>One clear picture.</span>
            </h1>

            <p className="subtitle">
              Upload your WhatsApp and Discord conversations.
              CentralResolve finds conflicting deadlines, ownership,
              project status, and unresolved decisions.
            </p>

            <button
              className="start-button"
              onClick={() => setShowUpload(true)}
            >
              Analyze Conversations
            </button>
          </div>
        </main>
      ) : (
        <main className="upload-page">
          <div className="upload-header">
            <p className="eyebrow">ANALYSIS WORKSPACE</p>

            <h2>Bring your conversations together.</h2>

            <p>
              Upload both conversation exports to find out where
              your team may not be on the same page.
            </p>
          </div>

          <div className="upload-grid">
            <FileUpload
              platform="WhatsApp"
              accept=".txt"
              file={whatsappFile}
              onFileSelect={setWhatsappFile}
            />

            <FileUpload
              platform="Discord"
              accept=".json"
              file={discordFile}
              onFileSelect={setDiscordFile}
            />
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button
            className="start-button analyze-button"
            disabled={!whatsappFile || !discordFile || loading}
            onClick={handleAnalyze}
          >
            {loading ? "Analyzing..." : "Analyze Conversations"}
          </button>
        </main>
      )}
    </div>
  );
}

export default App;