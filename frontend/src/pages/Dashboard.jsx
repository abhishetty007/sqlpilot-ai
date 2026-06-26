import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import ChatBox from "../components/ChatBox";

export default function Dashboard() {
  return (
    <div className="flex h-screen bg-zinc-950">

      <Sidebar />

      <div className="flex flex-1 flex-col">

        <Header />

        <ChatBox />

      </div>

    </div>
  );
}