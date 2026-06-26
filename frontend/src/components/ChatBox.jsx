import { Send, Paperclip } from "lucide-react";

export default function ChatBox() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center px-12">

      <div className="w-full max-w-4xl">

        <h1 className="text-center text-5xl font-bold text-white">
          Good Afternoon, ABHI 👋
        </h1>

        <p className="mt-4 mb-10 text-center text-zinc-500 text-lg">
          What would you like to query today?
        </p>

        {/* AI Input Box */}

        <div className="rounded-3xl border border-zinc-800 bg-zinc-900 p-6 shadow-2xl">

          <textarea
            rows="5"
            placeholder="Ask anything about your database..."
            className="
              w-full
              resize-none
              bg-transparent
              text-lg
              text-white
              placeholder:text-zinc-500
              outline-none
            "
          />

          <div className="mt-5 flex items-center justify-between">

            <button
              className="
                rounded-xl
                p-3
                transition
                hover:bg-zinc-800
              "
            >
              <Paperclip size={22} />
            </button>

            <button
              className="
                flex
                items-center
                gap-2
                rounded-xl
                bg-blue-600
                px-6
                py-3
                font-semibold
                transition
                hover:bg-blue-700
              "
            >
              <Send size={18} />
              Generate SQL
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}