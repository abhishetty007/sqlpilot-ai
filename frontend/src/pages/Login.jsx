import Logo from "../components/Logo";
import LoginCard from "../components/LoginCard";

export default function Login() {
  return (
    <div className="relative min-h-screen bg-zinc-950 flex overflow-hidden">

  {/* Blue Glow */}
  <div className="absolute left-0 top-0 h-[500px] w-[500px] rounded-full bg-blue-600/20 blur-[180px]" />

  {/* Purple Glow */}
  <div className="absolute right-0 bottom-0 h-[500px] w-[500px] rounded-full bg-purple-600/20 blur-[180px]" />
      
      {/* Left Side */}
      <div className="relative hidden lg:flex w-1/2 items-center justify-center z-10">
        <div className="max-w-lg">
          <Logo />
        </div>
      </div>

      {/* Right Side */}
      <div className="relative w-full lg:w-1/2 flex items-center justify-center z-10">
        <LoginCard />
      </div>

    </div>
  );
}