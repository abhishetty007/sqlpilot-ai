import { FcGoogle } from "react-icons/fc";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import CustomButton from "./CustomButton";
import CustomInput from "./CustomInput";

export default function LoginCard() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  async function handleLogin() {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/login",
        {
          username,
          password,
        }
      );

      console.log(response.data);

      navigate("/dashboard");

    } catch (error) {
      alert("Invalid username or password");
      console.error(error);
    }
  }

  return (
    <div className="w-full max-w-lg rounded-3xl border border-zinc-800 bg-zinc-900/80 backdrop-blur-xl p-12 shadow-2xl">

      <h2 className="text-5xl font-bold text-white">
  SQLPilot AI
</h2>

<p className="mt-2 text-zinc-400">
  Talk to your database naturally.
</p>

      <div className="mt-8 space-y-4">

        <button
          className="w-full flex items-center justify-center gap-3 rounded-xl bg-white py-3 font-semibold text-black transition-all duration-300 hover:scale-[1.02] hover:shadow-xl active:scale-95"
        >
          <FcGoogle size={24} />
          Continue with Google
        </button>

        <div className="flex items-center gap-4">
          <div className="h-px flex-1 bg-zinc-700"></div>
          <span className="text-sm text-zinc-500">OR</span>
          <div className="h-px flex-1 bg-zinc-700"></div>
        </div>

        <CustomInput
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <CustomInput
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <div onClick={handleLogin}>
          <CustomButton>
            Login
          </CustomButton>
        </div>

      </div>

      <p className="mt-8 text-center text-zinc-500">
        Don't have an account?{" "}
        <span className="cursor-pointer text-blue-400 hover:text-blue-300">
          Create Account
        </span>
      </p>

    </div>
  );
}