import {
  History,
  Settings,
  LogOut,
  Plus,
} from "lucide-react";

import { useRef, useState } from "react";

import DatabaseCard from "./DatabaseCard";

export default function Sidebar() {
  const databases = [
    {
      id: 1,
      name: "Hospital",
      status: "Connected",
    },
    {
      id: 2,
      name: "Student",
      status: "Connected",
    },
    {
      id: 3,
      name: "Library",
      status: "Connected",
    },
  ];

  const [selectedDatabase, setSelectedDatabase] = useState("Hospital");

  const fileInputRef = useRef(null);

  function handleDatabaseUpload(event) {
    const file = event.target.files[0];

    if (!file) return;

    alert(`Selected database: ${file.name}`);

    console.log(file);
  }

  return (
    <aside className="w-80 border-r border-zinc-800 bg-zinc-900 p-6 flex flex-col">

      {/* Logo */}

      <div>
        <h1 className="text-3xl font-bold text-white">
          SQLPilot AI
        </h1>

        <p className="mt-2 text-zinc-500">
          Intelligent Database Assistant
        </p>
      </div>

      {/* Databases */}

      <div className="mt-10">

        <h2 className="mb-4 text-sm font-semibold uppercase tracking-wider text-zinc-500">
          Databases
        </h2>

        <div className="space-y-3">

          {databases.map((db) => (
            <DatabaseCard
              key={db.id}
              name={db.name}
              status={db.status}
              selected={selectedDatabase === db.name}
              onClick={() => setSelectedDatabase(db.name)}
            />
          ))}

        </div>

        {/* Hidden File Input */}

        <input
          type="file"
          accept=".db,.sqlite,.sqlite3"
          ref={fileInputRef}
          onChange={handleDatabaseUpload}
          className="hidden"
        />

        {/* Upload Button */}

        <button
          onClick={() => fileInputRef.current.click()}
          className="
            mt-5
            flex
            w-full
            items-center
            justify-center
            gap-2
            rounded-2xl
            border
            border-dashed
            border-zinc-700
            py-3
            text-zinc-400
            transition
            hover:border-blue-500
            hover:text-white
          "
        >
          <Plus size={18} />
          Upload Database
        </button>

      </div>

      {/* Bottom */}

      <div className="mt-auto space-y-2">

        <button className="flex w-full items-center gap-3 rounded-xl px-4 py-3 hover:bg-zinc-800">
          <History size={20} />
          Query History
        </button>

        <button className="flex w-full items-center gap-3 rounded-xl px-4 py-3 hover:bg-zinc-800">
          <Settings size={20} />
          Settings
        </button>

        <button className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-red-400 hover:bg-red-500/10">
          <LogOut size={20} />
          Logout
        </button>

      </div>

    </aside>
  );
}