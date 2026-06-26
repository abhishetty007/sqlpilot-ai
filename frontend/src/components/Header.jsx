export default function Header() {
  return (
    <header className="flex items-center justify-between border-b border-zinc-800 px-10 py-6">

      <div>
        <h2 className="text-3xl font-bold text-white">
          SQLPilot AI
        </h2>

        <p className="mt-1 text-zinc-500">
          Your AI-powered database copilot.
        </p>
      </div>

      <div className="flex items-center gap-4">

        <div className="text-right">
          <p className="text-sm text-zinc-500">
            Logged in as
          </p>

          <p className="font-semibold text-white">
            ABHI
          </p>
        </div>

        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-600 text-lg font-bold">
          A
        </div>

      </div>

    </header>
  );
}