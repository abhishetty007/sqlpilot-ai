import { useState, useEffect, useRef } from "react";

export default function ChatBox({ selectedDatabase }) {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  // Automatically scroll to the newest message/result
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages, loading]);

  const generateAndExecute = async () => {
    if (!prompt.trim() || loading) return;

    const userPrompt = prompt.trim();

    setPrompt("");

    // Add user message immediately
    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        content: userPrompt,
      },
    ]);

    setLoading(true);

    try {
      // ==========================================
      // GENERATE SQL
      // ==========================================

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

      const sql = generateData.sql;

      // ==========================================
      // EXECUTE SQL AUTOMATICALLY
      // ==========================================

      const executeResponse = await fetch(
        "http://127.0.0.1:8000/execute-sql",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            database: selectedDatabase,
            sql: sql,
          }),
        }
      );

      const executeData = await executeResponse.json();

      if (!executeResponse.ok) {
        throw new Error(
          executeData.detail || "Failed to execute SQL."
        );
      }

      // ==========================================
      // ADD AI RESPONSE
      // ==========================================

      setMessages((prev) => [
        ...prev,
        {
          type: "assistant",
          sql: sql,
          rows: executeData.rows || [],
        },
      ]);
    } catch (error) {
      console.error("Chat error:", error);

      setMessages((prev) => [
        ...prev,
        {
          type: "error",
          content:
            error.message || "Something went wrong.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // ==========================================
  // ENTER KEY
  // ==========================================

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      generateAndExecute();
    }
  };

  return (
    <div className="flex min-h-0 flex-1 flex-col bg-zinc-950">

      {/* ======================================
          CHAT MESSAGES
      ====================================== */}

      <div className="min-h-0 flex-1 overflow-y-auto px-4 py-6">

        <div className="mx-auto flex w-full max-w-4xl flex-col gap-6">

          {/* Empty state */}
          {messages.length === 0 && !loading && (
            <div className="flex flex-1 items-center justify-center py-32">

              <div className="text-center">

                <h2 className="text-2xl font-semibold text-white">
                  Ask SQLPilot anything
                </h2>

                <p className="mt-2 text-zinc-500">
                  Ask questions about your database in natural language.
                </p>

                <div className="mt-6 flex flex-wrap justify-center gap-2">

                  <button
                    onClick={() =>
                      setPrompt("Show all customers")
                    }
                    className="rounded-xl border border-zinc-800 bg-zinc-900 px-4 py-2 text-sm text-zinc-300 transition hover:border-zinc-600 hover:bg-zinc-800"
                  >
                    Show all customers
                  </button>

                  <button
                    onClick={() =>
                      setPrompt("Show all films")
                    }
                    className="rounded-xl border border-zinc-800 bg-zinc-900 px-4 py-2 text-sm text-zinc-300 transition hover:border-zinc-600 hover:bg-zinc-800"
                  >
                    Show all films
                  </button>

                  <button
                    onClick={() =>
                      setPrompt("Show all actors")
                    }
                    className="rounded-xl border border-zinc-800 bg-zinc-900 px-4 py-2 text-sm text-zinc-300 transition hover:border-zinc-600 hover:bg-zinc-800"
                  >
                    Show all actors
                  </button>

                </div>

              </div>

            </div>
          )}

          {/* ====================================
              MESSAGES
          ==================================== */}

          {messages.map((message, index) => (

            <div key={index}>

              {/* USER MESSAGE */}
              {message.type === "user" && (
                <div className="flex justify-end">

                  <div className="max-w-[80%] rounded-2xl rounded-br-md bg-blue-600 px-5 py-3 text-white shadow-lg">

                    <p className="whitespace-pre-wrap break-words">
                      {message.content}
                    </p>

                  </div>

                </div>
              )}

              {/* ASSISTANT RESPONSE */}
              {message.type === "assistant" && (
                <div className="mt-4 flex justify-start">

                  <div className="w-full max-w-4xl">

                    {/* SQL */}
                    <div className="overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900">

                      <div className="flex items-center justify-between border-b border-zinc-800 px-4 py-3">

                        <span className="text-sm font-medium text-zinc-300">
                          Generated SQL
                        </span>

                        <button
                          onClick={() =>
                            navigator.clipboard.writeText(
                              message.sql
                            )
                          }
                          className="rounded-lg px-3 py-1.5 text-xs text-zinc-400 transition hover:bg-zinc-800 hover:text-white"
                        >
                          Copy
                        </button>

                      </div>

                      <pre className="overflow-x-auto p-4 text-sm leading-6 text-green-400">
                        <code>{message.sql}</code>
                      </pre>

                    </div>

                    {/* RESULTS */}
                    <div className="mt-4 overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900">

                      <div className="border-b border-zinc-800 px-4 py-3">

                        <span className="text-sm font-medium text-zinc-300">
                          Query Results
                        </span>

                      </div>

                      {message.rows.length === 0 ? (

                        <div className="p-6 text-sm text-zinc-500">
                          Query executed successfully. No rows returned.
                        </div>

                      ) : (

                        <div className="max-h-[500px] overflow-auto">

                          <table className="w-full border-collapse text-sm">

                            <thead className="sticky top-0 bg-zinc-900">

                              <tr>

                                {Object.keys(message.rows[0]).map(
                                  (column) => (
                                    <th
                                      key={column}
                                      className="whitespace-nowrap border-b border-zinc-800 px-4 py-3 text-left font-medium text-zinc-400"
                                    >
                                      {column}
                                    </th>
                                  )
                                )}

                              </tr>

                            </thead>

                            <tbody>

                              {message.rows.map(
                                (row, rowIndex) => (

                                  <tr
                                    key={rowIndex}
                                    className="transition hover:bg-zinc-800/50"
                                  >

                                    {Object.keys(
                                      message.rows[0]
                                    ).map((column) => (

                                      <td
                                        key={column}
                                        className="whitespace-nowrap border-b border-zinc-800/70 px-4 py-3 text-zinc-300"
                                      >
                                        {row[column] === null
                                          ? "NULL"
                                          : String(
                                              row[column]
                                            )}
                                      </td>

                                    ))}

                                  </tr>

                                )
                              )}

                            </tbody>

                          </table>

                        </div>

                      )}

                    </div>

                  </div>

                </div>
              )}

              {/* ERROR */}
              {message.type === "error" && (
                <div className="mt-4 flex justify-start">

                  <div className="max-w-[80%] rounded-2xl border border-red-900/50 bg-red-950/30 px-5 py-4 text-sm text-red-300">

                    {message.content}

                  </div>

                </div>
              )}

            </div>

          ))}

          {/* ====================================
              LOADING
          ==================================== */}

          {loading && (
            <div className="flex justify-start">

              <div className="rounded-2xl border border-zinc-800 bg-zinc-900 px-5 py-4">

                <div className="flex items-center gap-3">

                  <div className="flex gap-1">

                    <span className="h-2 w-2 animate-bounce rounded-full bg-zinc-500 [animation-delay:-0.3s]" />

                    <span className="h-2 w-2 animate-bounce rounded-full bg-zinc-500 [animation-delay:-0.15s]" />

                    <span className="h-2 w-2 animate-bounce rounded-full bg-zinc-500" />

                  </div>

                  <span className="text-sm text-zinc-400">
                    Thinking...
                  </span>

                </div>

              </div>

            </div>
          )}

          {/* Scroll target */}
          <div ref={chatEndRef} />

        </div>

      </div>


      {/* ======================================
          INPUT AREA
      ====================================== */}

      <div className="border-t border-zinc-800 bg-zinc-950 px-4 py-4">

        <div className="mx-auto w-full max-w-4xl">

          <div className="relative flex items-end rounded-2xl border border-zinc-800 bg-zinc-900 shadow-xl transition focus-within:border-zinc-600">

            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={`Ask about ${selectedDatabase}...`}
              disabled={loading}
              rows={1}
              className="max-h-40 min-h-[52px] flex-1 resize-none bg-transparent px-4 py-4 pr-14 text-sm text-white outline-none placeholder:text-zinc-600 disabled:cursor-not-allowed disabled:opacity-50"
            />

            <button
              onClick={generateAndExecute}
              disabled={!prompt.trim() || loading}
              className="absolute bottom-2 right-2 flex h-9 w-9 items-center justify-center rounded-xl bg-blue-600 text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:bg-zinc-800 disabled:text-zinc-600"
              title="Generate and execute"
            >
              ↑
            </button>

          </div>

          <p className="mt-2 text-center text-xs text-zinc-600">
            Press Enter to generate and execute • Shift + Enter for new line
          </p>

        </div>

      </div>

    </div>
  );
}