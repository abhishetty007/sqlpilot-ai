import { Database } from "lucide-react";

export default function DatabaseCard({
  name,
  status,
  selected,
  onClick,
}) {
  return (
    <div
      onClick={onClick}
      className={`
        cursor-pointer
        rounded-2xl
        border
        p-4
        transition-all
        hover:scale-[1.02]

        ${
          selected
            ? "border-blue-500 bg-blue-500/10"
            : "border-zinc-800 bg-zinc-900 hover:border-blue-500 hover:bg-zinc-800"
        }
      `}
    >
      <div className="flex items-center gap-3">

        <div
          className={`
            rounded-xl
            p-3

            ${
              selected
                ? "bg-blue-600"
                : "bg-zinc-700"
            }
          `}
        >
          <Database size={22} />
        </div>

        <div>

          <h3 className="font-semibold text-white">
            {name}
          </h3>

          <p className="text-sm text-green-400">
            {status}
          </p>

        </div>

      </div>

    </div>
  );
}