export default function Logo() {
  return (
    <div className="text-center">

      <img
        src="/logo-dark.png"
        alt="SQLPilot AI"
        className="mx-auto w-72 drop-shadow-2xl"
      />

      <h1 className="mt-8 text-6xl font-extrabold text-white tracking-tight">
        SQLPilot AI
      </h1>

      <p className="mt-4 text-xl text-zinc-400">
        Talk to your database naturally.
      </p>

      <div className="mt-10 rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6 backdrop-blur">

        <p className="text-zinc-300 text-lg leading-8">
          🚀 AI-powered SQL generation
          <br />
          📊 Execute queries instantly
          <br />
          🗄️ Connect multiple databases
          <br />
          ⚡ FastAPI + React + AI
        </p>

      </div>

    </div>
  );
}