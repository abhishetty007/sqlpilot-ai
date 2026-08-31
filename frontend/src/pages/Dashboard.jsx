import { useState } from "react";

import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import ChatBox from "../components/ChatBox";

export default function Dashboard() {

  const [selectedDatabase, setSelectedDatabase] = useState("sakila");

  return (

    <div className="flex h-screen bg-zinc-950 text-white">

      <Sidebar
        selectedDatabase={selectedDatabase}
        setSelectedDatabase={setSelectedDatabase}
      />

      <div className="flex min-w-0 flex-1 flex-col">

        <Header />

        <ChatBox
          selectedDatabase={selectedDatabase}
        />

      </div>

    </div>

  );
}