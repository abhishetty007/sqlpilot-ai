import {
  Send,
  Paperclip,
  Database,
  Sparkles,
  Copy,
  Check,
  Clock,
  Rows3,
} from "lucide-react";

import { useState } from "react";

export default function ChatBox({ selectedDatabase = "Hospital" }) {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // =====================================================
  // GENERATE SQL + EXECUTE AUTOMATICALLY
  // =====================================================

  async function generateAndExecute() {
    if (!prompt.trim() || loading) return;

    const userPrompt = prompt.trim();

    // Immediately show user's message
    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        prompt: userPrompt,
      },
    ]);

    setPrompt("");
    setLoading(true);

    try {
      // =================================================
      // STEP 1: GENERATE SQL
      // =================================================

      const generateResponse = await fetch(
        "http://127.0.0.1:8000/generate-sql",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            prompt: userPrompt,
            database: selectedDatabase,
          }),
        }
      );

      const generateData = await generateResponse.json();

      if (!generateResponse.ok) {
        throw new Error(
          generateData.detail || "Failed to generate SQL."
        );
      }

      if (!generateData.success || !generateData.sql) {
        throw new Error("No SQL generated.");
      }

      const generatedSQL = generateData.sql;

      // =================================================
      // STEP 2: EXECUTE SQL
      // =================================================

      const start = performance.now();

      const executeResponse = await fetch(
        "http://127.0.0.1:8000/execute-sql",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            database: selectedDatabase,
            sql: generatedSQL,
          }),
        }
      );

      const executeData = await executeResponse.json();

      const end = performance.now();

      const executionTime = (
        (end - start) /
        1000
      ).toFixed(3);

      if (!executeResponse.ok) {
        throw new Error(
          executeData.detail || "SQL execution failed."
        );
      }

      // =================================================
      // ADD AI RESPONSE TO CHAT
      // =================================================

      setMessages((prev) => [
        ...prev,
        {
          type: "assistant",
          sql: generatedSQL,
          rows: executeData.rows || [],
          executionTime,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          type: "error",
          message:
            error.message ||
            "Unable to connect to the SQLPilot server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  // =====================================================
  // ENTER KEY
  // =====================================================

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      generateAndExecute();
    }
  }

  // =====================================================
  // COPY SQL
  // =====================================================

  function SQLBlock({ sql }) {
    const [copied, setCopied] = useState(false);

    async function copySQL() {
      try {
        await navigator.clipboard.writeText(sql);

        setCopied(true);

        setTimeout(() => {
          setCopied(false);
        }, 1500);
      } catch (error) {
        console.error(error);
      }
    }

    return (
      <div className="mt-4 overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-950">
        <div className="flex items-center justify-between border-b border-zinc-800 px-4 py-3">
          <div className="flex items-center gap-2">
            <Sparkles
              size={15}
              className="text-blue-400"
            />

            <span className="text-xs font-semibold text-zinc-400">
              Generated SQL
            </span>
          </div>

          <button
            onClick={copySQL}
            className="flex items-center gap-2 rounded-lg px-3 py-1.5 text-xs text-zinc-500 transition hover:bg-zinc-800 hover:text-white"
          >
            {copied ? (
              <>
                <Check size={14} />
                Copied
              </>
            ) : (
              <>
                <Copy size={14} />
                Copy
              </>
            )}
          </button>
        </div>

        <pre className="overflow-x-auto p-4 text-sm leading-relaxed text-emerald-400">
          <code>{sql}</code>
        </pre>
      </div>
    );
  }

  // =====================================================
  // RESULTS TABLE
  // =====================================================

  function ResultsTable({ rows, executionTime }) {
    if (!rows || rows.length === 0) {
      return (
        <div className="mt-4 rounded-2xl border border-zinc-800 bg-zinc-950 p-5">
          <div className="flex items-center gap-2 text-sm text-zinc-400">
            <Rows3 size={17} />
            Query executed successfully — no rows returned.
          </div>
        </div>
      );
    }

    const columns = Object.keys(rows[0]);

    return (
      <div className="mt-4 overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-950">
        {/* Result Header */}

        <div className="flex items-center justify-between border-b border-zinc-800 px-4 py-3">
          <div className="flex items-center gap-2">
            <Rows3
              size={17}
              className="text-blue-400"
            />

            <span className="text-xs font-semibold text-zinc-300">
              Query Results
            </span>

            <span className="text-xs text-zinc-600">
              {rows.length} row
              {rows.length !== 1 ? "s" : ""}
            </span>
          </div>

          <div className="flex items-center gap-2 text-xs text-zinc-600">
            <Clock size={13} />
            {executionTime}s
          </div>
        </div>

        {/* Table */}

        <div className="max-h-[420px] overflow-auto">
          <table className="w-full text-left text-sm">
            <thead className="sticky top-0 bg-zinc-900">
              <tr className="border-b border-zinc-800">
                {columns.map((column) => (
                  <th
                    key={column}
                    className="whitespace-nowrap px-4 py-3 text-xs font-semibold uppercase tracking-wider text-zinc-500"
                  >
                    {column}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {rows.map((row, index) => (
                <tr
                  key={index}
                  className="border-b border-zinc-900 hover:bg-zinc-900"
                >
                  {columns.map((column) => (
                    <td
                      key={column}
                      className="whitespace-nowrap px-4 py-3 text-zinc-300"
                    >
                      {String(row[column] ?? "NULL")}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  // =====================================================
  // UI
  // =====================================================

  return (
    <main className="flex min-h-0 flex-1 flex-col bg-zinc-950">

      {/* =================================================
          CHAT AREA
      ================================================= */}

      <div className="min-h-0 flex-1 overflow-y-auto px-6 py-8">

        <div className="mx-auto w-full max-w-4xl">

          {/* Empty State */}

          {messages.length === 0 && !loading && (
            <div className="flex min-h-[55vh] flex-col items-center justify-center text-center">

              <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl border border-blue-500/20 bg-blue-500/10">
                <Sparkles
                  size={28}
                  className="text-blue-400"
                />
              </div>

              <h1 className="text-4xl font-bold text-white">
                Ask your database
              </h1>

              <p className="mt-3 max-w-lg text-zinc-500">
                Ask a question in plain English.
                SQLPilot will generate the SQL and
                run it automatically.
              </p>

              <div className="mt-6 flex items-center gap-2 rounded-full border border-zinc-800 bg-zinc-900 px-4 py-2 text-xs text-zinc-500">
                <Database size={14} />
                {selectedDatabase}
              </div>

            </div>
          )}

          {/* =================================================
              MESSAGES
          ================================================= */}

          <div className="space-y-8">

            {messages.map((message, index) => (

              <div key={index}>

                {/* USER MESSAGE */}

                {message.type === "user" && (
                  <div className="flex justify-end">

                    <div className="max-w-[75%] rounded-3xl bg-blue-600 px-5 py-3.5 text-sm leading-relaxed text-white shadow-lg">
                      {message.prompt}
                    </div>

                  </div>
                )}

                {/* AI RESPONSE */}

                {message.type === "assistant" && (
                  <div className="mt-3 flex gap-4">

                    {/* AI ICON */}

                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-500/10">
                      <Sparkles
                        size={18}
                        className="text-blue-400"
                      />
                    </div>

                    {/* RESPONSE */}

                    <div className="min-w-0 flex-1">

                      <div className="mb-2 flex items-center gap-2">
                        <span className="text-sm font-semibold text-white">
                          SQLPilot AI
                        </span>

                        <span className="text-xs text-zinc-600">
                          {selectedDatabase}
                        </span>
                      </div>

                      <SQLBlock sql={message.sql} />

                      <ResultsTable
                        rows={message.rows}
                        executionTime={
                          message.executionTime
                        }
                      />

                    </div>

                  </div>
                )}

                {/* ERROR */}

                {message.type === "error" && (
                  <div className="mt-3 flex gap-4">

                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-red-500/10">
                      <Sparkles
                        size={18}
                        className="text-red-400"
                      />
                    </div>

                    <div className="rounded-2xl border border-red-500/20 bg-red-500/5 px-5 py-4 text-sm text-red-300">
                      {message.message}
                    </div>

                  </div>
                )}

              </div>

            ))}

            {/* LOADING */}

            {loading && (
              <div className="flex gap-4">

                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-500/10">
                  <Sparkles
                    size={18}
                    className="animate-pulse text-blue-400"
                  />
                </div>

                <div className="flex items-center gap-2 rounded-2xl border border-zinc-800 bg-zinc-900 px-5 py-4 text-sm text-zinc-500">

                  <span className="animate-pulse">
                    Thinking...
                  </span>

                  <span className="text-zinc-700">
                    •
                  </span>

                  <span className="animate-pulse">
                    Running query...
                  </span>

                </div>

              </div>
            )}

          </div>

        </div>

      </div>

      {/* =================================================
          FIXED INPUT AREA
      ================================================= */}

      <div className="border-t border-zinc-800 bg-zinc-950 px-6 py-4">

        <div className="mx-auto w-full max-w-4xl">

          {/* Database indicator */}

          <div className="mb-2 flex items-center gap-2 px-2 text-xs text-zinc-600">

            <span className="h-2 w-2 rounded-full bg-emerald-400" />

            Using {selectedDatabase}

          </div>

          {/* Input */}

          <div className="rounded-3xl border border-zinc-800 bg-zinc-900 p-3 shadow-2xl transition focus-within:border-blue-500/40">

            <textarea
              rows={1}
              value={prompt}
              onChange={(e) =>
                setPrompt(e.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Ask your database..."
              disabled={loading}
              className="max-h-32 min-h-[44px] w-full resize-none bg-transparent px-3 py-2.5 text-sm leading-relaxed text-white outline-none placeholder:text-zinc-600 disabled:opacity-50"
            />

            <div className="mt-2 flex items-center justify-between">

              <button
                type="button"
                className="rounded-xl p-2.5 text-zinc-600 transition hover:bg-zinc-800 hover:text-zinc-300"
              >
                <Paperclip size={18} />
              </button>

              <button
                onClick={generateAndExecute}
                disabled={
                  loading ||
                  !prompt.trim()
                }
                className="flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-40"
              >
                <Send size={16} />

                {loading
                  ? "Running..."
                  : "Ask"}
              </button>

            </div>

          </div>

          <p className="mt-2 text-center text-[11px] text-zinc-700">
            Enter to send • Shift + Enter for a new line
          </p>

        </div>

      </div>

    </main>
  );
}