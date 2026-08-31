import { FcGoogle } from "react-icons/fc";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import CustomButton from "./CustomButton";
import CustomInput from "./CustomInput";

export default function LoginCard() {

  const navigate = useNavigate();

  const [isSignup, setIsSignup] = useState(false);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");


  // =========================================================
  // LOGIN
  // =========================================================

  async function handleLogin() {

    if (!username || !password) {

      setError(
        "Please enter your username and password."
      );

      return;
    }

    try {

      setLoading(true);
      setError("");
      setSuccess("");

      const response = await axios.post(
        "http://127.0.0.1:8000/login",
        {
          username,
          password,
        }
      );

      const user = response.data;

      localStorage.setItem(
        "sqlpilot_user",
        JSON.stringify({
          user_id: user.user_id,
          username: user.username,
        })
      );

      navigate("/dashboard");

    } catch (error) {

      console.error(error);

      if (error.response?.status === 401) {

        setError(
          "Invalid username or password."
        );

      } else {

        setError(
          "Unable to connect to the SQLPilot server."
        );
      }

    } finally {

      setLoading(false);

    }
  }


  // =========================================================
  // CREATE ACCOUNT
  // =========================================================

  async function handleSignup() {

    if (!username || !password) {

      setError(
        "Please enter a username and password."
      );

      return;
    }

    if (username.length < 3) {

      setError(
        "Username must be at least 3 characters."
      );

      return;
    }

    if (password.length < 6) {

      setError(
        "Password must be at least 6 characters."
      );

      return;
    }

    try {

      setLoading(true);
      setError("");
      setSuccess("");

      const response = await axios.post(
        "http://127.0.0.1:8000/register",
        {
          username,
          password,
        }
      );

      setSuccess(
        response.data.message ||
        "Account created successfully!"
      );

      setUsername("");
      setPassword("");

      // Switch back to login after successful signup
      setTimeout(() => {

        setIsSignup(false);
        setSuccess("");

      }, 1200);

    } catch (error) {

      console.error(error);

      if (error.response?.status === 400) {

        const message =
          error.response?.data?.detail;

        if (
          message &&
          message.toLowerCase().includes("unique")
        ) {

          setError(
            "Username already exists."
          );

        } else {

          setError(
            message || "Unable to create account."
          );
        }

      } else {

        setError(
          "Unable to connect to the SQLPilot server."
        );
      }

    } finally {

      setLoading(false);

    }
  }


  // =========================================================
  // SWITCH LOGIN / SIGNUP
  // =========================================================

  function switchMode() {

    setIsSignup(!isSignup);

    setUsername("");
    setPassword("");
    setError("");
    setSuccess("");
  }


  return (

    <div className="
      w-full
      max-w-lg
      rounded-3xl
      border
      border-zinc-800
      bg-zinc-900/80
      backdrop-blur-xl
      p-12
      shadow-2xl
    ">

      {/* Header */}

      <div>

        <h2 className="
          text-5xl
          font-bold
          tracking-tight
          text-white
        ">
          SQLPilot AI
        </h2>

        <p className="
          mt-3
          text-zinc-400
          text-lg
        ">
          Talk to your database naturally.
        </p>

      </div>


      {/* Form */}

      <div className="mt-8 space-y-4">


        {/* Google */}

        <button
          type="button"
          className="
            w-full
            flex
            items-center
            justify-center
            gap-3
            rounded-xl
            bg-white
            py-3
            font-semibold
            text-black
            transition-all
            duration-300
            hover:scale-[1.02]
            hover:shadow-xl
            active:scale-95
          "
        >

          <FcGoogle size={24} />

          Continue with Google

        </button>


        {/* Divider */}

        <div className="
          flex
          items-center
          gap-4
          py-2
        ">

          <div className="h-px flex-1 bg-zinc-700" />

          <span className="text-sm text-zinc-500">
            OR
          </span>

          <div className="h-px flex-1 bg-zinc-700" />

        </div>


        {/* Username */}

        <CustomInput
          placeholder="Username"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
        />


        {/* Password */}

        <CustomInput
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />


        {/* Error */}

        {error && (

          <div className="
            rounded-xl
            border
            border-red-500/20
            bg-red-500/10
            px-4
            py-3
            text-sm
            text-red-400
          ">

            {error}

          </div>

        )}


        {/* Success */}

        {success && (

          <div className="
            rounded-xl
            border
            border-green-500/20
            bg-green-500/10
            px-4
            py-3
            text-sm
            text-green-400
          ">

            {success}

          </div>

        )}


        {/* Main Button */}

        <div
          onClick={
            loading
              ? undefined
              : isSignup
                ? handleSignup
                : handleLogin
          }
        >

          <CustomButton>

            {loading
              ? (
                isSignup
                  ? "Creating account..."
                  : "Signing in..."
              )
              : (
                isSignup
                  ? "Create Account"
                  : "Login"
              )
            }

          </CustomButton>

        </div>

      </div>


      {/* Switch Login / Signup */}

      <p className="
        mt-8
        text-center
        text-zinc-500
      ">

        {isSignup
          ? "Already have an account?"
          : "Don't have an account?"
        }

        {" "}

        <button
          type="button"
          onClick={switchMode}
          className="
            text-blue-400
            hover:text-blue-300
            transition
          "
        >

          {isSignup
            ? "Login"
            : "Create Account"
          }

        </button>

      </p>

    </div>

  );
}