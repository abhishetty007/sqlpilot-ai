import {
  History,
  Settings,
  LogOut,
  Plus,
  Database,
  ChevronDown,
  Table2,
} from "lucide-react";

import { useEffect, useRef, useState } from "react";

import DatabaseCard from "./DatabaseCard";

export default function Sidebar({
  selectedDatabase,
  setSelectedDatabase,
}) {
  const [tables, setTables] = useState([]);
  const [databases, setDatabases] = useState([]);

  const fileInputRef = useRef(null);


  async function loadDatabases() {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/databases"
      );

      const data = await response.json();

      setDatabases(
        data.map((db, index) => ({
          id: index,
          name: db.name,
          status: "Connected",
        }))
      );

    } catch (error) {

      console.error("Failed to load databases:", error);

    }
  }


  async function loadTables(databaseName) {

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/tables/${databaseName}.db`
      );

      const data = await response.json();

      setTables(data.tables || []);

    } catch (error) {

      console.error("Failed to load tables:", error);

      setTables([]);

    }
  }


  useEffect(() => {

    loadDatabases();

  }, []);


  useEffect(() => {

    if (selectedDatabase) {
      loadTables(selectedDatabase);
    }

  }, [selectedDatabase]);


  async function handleDatabaseUpload(event) {

    const file = event.target.files[0];

    if (!file) return;

    try {

      const formData = new FormData();

      formData.append("file", file);

      const response = await fetch(
        "http://127.0.0.1:8000/upload-database",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {

        alert(data.detail || "Upload failed.");

        return;
      }

      alert(data.message);

      await loadDatabases();

    } catch (error) {

      console.error(error);

      alert("Failed to upload database.");

    }

    event.target.value = "";
  }


  function handleLogout() {

    localStorage.removeItem("sqlpilot_user");

    window.location.href = "/";

  }
async function handleDatabaseDelete(databaseName) {

  const confirmed = window.confirm(
    `Are you sure you want to remove "${databaseName}"?`
  );

  if (!confirmed) {
    return;
  }

  try {

    const response = await fetch(
      `http://127.0.0.1:8000/databases/${databaseName}.db`,
      {
        method: "DELETE",
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to remove database."
      );
    }

    alert(data.message);

    // Refresh database list
    await loadDatabases();

    // If deleted database was selected
    if (selectedDatabase === databaseName) {

      setSelectedDatabase("");

      setTables([]);
    }

  } catch (error) {

    console.error(error);

    alert(
      error.message ||
      "Failed to remove database."
    );
  }
}

  return (

    <aside className="
      flex
      h-screen
      w-80
      flex-shrink-0
      flex-col
      border-r
      border-zinc-800/80
      bg-zinc-950
      px-5
      py-6
    ">


      {/* ═══════════════════════════════════════
          LOGO
      ═══════════════════════════════════════ */}

      <div className="px-2">

        <div className="flex items-center gap-3">

          <div className="
            flex
            h-10
            w-10
            items-center
            justify-center
            rounded-xl
            bg-blue-600
            shadow-lg
            shadow-blue-600/20
          ">

            <Database
              size={21}
              className="text-white"
            />

          </div>

          <div>

            <h1 className="
              text-lg
              font-bold
              tracking-tight
              text-white
            ">
              SQLPilot AI
            </h1>

            <p className="text-xs text-zinc-500">
              Database Copilot
            </p>

          </div>

        </div>

      </div>


      {/* ═══════════════════════════════════════
          DATABASE SECTION
      ═══════════════════════════════════════ */}

      <div className="mt-10 flex-1 overflow-y-auto pr-1">

        <div className="
          mb-4
          flex
          items-center
          justify-between
          px-2
        ">

          <h2 className="
            text-xs
            font-semibold
            uppercase
            tracking-[0.15em]
            text-zinc-500
          ">
            Databases
          </h2>

          <span className="
            rounded-md
            bg-zinc-900
            px-2
            py-1
            text-[10px]
            font-medium
            text-zinc-500
          ">
            {databases.length}
          </span>

        </div>


        <div className="space-y-2">

          {databases.map((db) => (

            <DatabaseCard
  key={db.id}
  name={db.name}
  status={db.status}
  selected={selectedDatabase === db.name}
  onClick={() => {
    setSelectedDatabase(db.name);
    loadTables(db.name);
  }}
  onDelete={handleDatabaseDelete}
/>

          ))}

        </div>


        {/* ═══════════════════════════════════════
            UPLOAD DATABASE
        ═══════════════════════════════════════ */}

        <input
          type="file"
          accept=".db,.sqlite,.sqlite3"
          ref={fileInputRef}
          onChange={handleDatabaseUpload}
          className="hidden"
        />

        <button
          onClick={() => fileInputRef.current?.click()}
          className="
            mt-4
            flex
            w-full
            items-center
            justify-center
            gap-2
            rounded-xl
            border
            border-dashed
            border-zinc-800
            bg-zinc-900/30
            py-3
            text-sm
            font-medium
            text-zinc-500
            transition-all
            duration-200
            hover:border-blue-500/50
            hover:bg-blue-500/5
            hover:text-zinc-200
          "
        >

          <Plus size={17} />

          Upload Database

        </button>


        {/* ═══════════════════════════════════════
            TABLES
        ═══════════════════════════════════════ */}

        {selectedDatabase && (

          <div className="mt-8">

            <div className="
              mb-3
              flex
              items-center
              justify-between
              px-2
            ">

              <div className="flex items-center gap-2">

                <Table2
                  size={14}
                  className="text-zinc-600"
                />

                <p className="
                  text-xs
                  font-semibold
                  uppercase
                  tracking-[0.15em]
                  text-zinc-500
                ">
                  Tables
                </p>

              </div>

              <ChevronDown
                size={14}
                className="text-zinc-600"
              />

            </div>


            {tables.length > 0 ? (

              <div className="space-y-1">

                {tables.map((table) => (

                  <button
                    key={table}
                    className="
                      flex
                      w-full
                      items-center
                      gap-3
                      rounded-lg
                      px-3
                      py-2
                      text-left
                      text-sm
                      text-zinc-500
                      transition
                      hover:bg-zinc-900
                      hover:text-zinc-200
                    "
                  >

                    <Table2
                      size={15}
                      className="text-zinc-700"
                    />

                    <span className="truncate">
                      {table}
                    </span>

                  </button>

                ))}

              </div>

            ) : (

              <p className="
                px-3
                text-xs
                text-zinc-700
              ">
                No tables found
              </p>

            )}

          </div>

        )}

      </div>


      {/* ═══════════════════════════════════════
          BOTTOM NAVIGATION
      ═══════════════════════════════════════ */}

      <div className="
        mt-5
        border-t
        border-zinc-900
        pt-4
      ">

        <button className="
          flex
          w-full
          items-center
          gap-3
          rounded-xl
          px-3
          py-3
          text-sm
          text-zinc-500
          transition
          hover:bg-zinc-900
          hover:text-white
        ">

          <History size={18} />

          Query History

        </button>


        <button className="
          flex
          w-full
          items-center
          gap-3
          rounded-xl
          px-3
          py-3
          text-sm
          text-zinc-500
          transition
          hover:bg-zinc-900
          hover:text-white
        ">

          <Settings size={18} />

          Settings

        </button>


        <button
          onClick={handleLogout}
          className="
            mt-1
            flex
            w-full
            items-center
            gap-3
            rounded-xl
            px-3
            py-3
            text-sm
            text-red-400/70
            transition
            hover:bg-red-500/5
            hover:text-red-400
          "
        >

          <LogOut size={18} />

          Logout

        </button>

      </div>

    </aside>

  );
}            