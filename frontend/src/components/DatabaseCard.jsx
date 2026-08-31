import { Database, Trash2 } from "lucide-react";

export default function DatabaseCard({
  name,
  status,
  selected,
  onClick,
  onDelete,
}) {
  function handleDelete(event) {
    event.stopPropagation();

    onDelete(name);
  }

  return (
    <div
      onClick={onClick}
      className={`
        group
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

        {/* Database Icon */}

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


        {/* Database Info */}

        <div className="min-w-0 flex-1">

          <h3 className="truncate font-semibold text-white">
            {name}
          </h3>

          <p className="text-sm text-green-400">
            {status}
          </p>

        </div>


        {/* Delete Button */}

        <button
          onClick={handleDelete}
          title="Remove database"
          className="
            rounded-lg
            p-2
            text-zinc-500
            opacity-0
            transition-all
            group-hover:opacity-100
            hover:bg-red-500/10
            hover:text-red-400
          "
        >
          <Trash2 size={18} />
        </button>

      </div>

    </div>
  );
}