import { useState } from "react";
import ShowHidePassword from "./ShowHidePassword";
import Calendar from "./Calendar";
import { Link } from "react-router-dom";

export default function AuthForm() {
  const [tab, setTab] = useState<"signin" | "signup">("signin");
  const [emailOrUsername, setEmailOrUserName] = useState("");
  const [password, setPassword] = useState("");

  {
    /* API SignIn */
  }
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:5000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: emailOrUsername,
          password: password,
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        console.error("Login failed:", data);
        return;
      }

      console.log("Login success:", data);

      localStorage.setItem("token", data.token);
    } catch (err) {
      console.error("Error:", err);
    }
  };

  return (
    <div className="w-full px-40">
      <div className="bg-white border-3 border-[#D0A2F7] rounded-[10px] p-8 w-[450px] my-12">
        {/* Tab */}
        <div className="flex justify-center mb-6 gap-18">
          <button
            onClick={() => setTab("signin")}
            className={`px-6 py-2 h-14 w-38 rounded-[10px] font-semibold duration-75 ease-in-out ${
              tab === "signin"
                ? "bg-[#8F87F1] text-white"
                : "hover:bg-[#F5F5F0] cursor-pointer duration-150 ease-in-out"
            }`}
          >
            SIGN IN
          </button>
          <button
            onClick={() => setTab("signup")}
            className={`px-6 py-2 h-14 w-38 rounded-[10px] font-semibold duration-75 ease-in-out ${
              tab === "signup"
                ? "bg-[#8F87F1] text-white"
                : "hover:bg-[#F5F5F0] cursor-pointer duration-150 ease-in-out"
            }`}
          >
            SIGN UP
          </button>
        </div>

        {/* Sign in From */}
        {tab === "signin" && (
          <form
            className="space-y-4 duration-75 ease-in-out"
            onSubmit={handleLogin}
          >
            {/* Username, email box */}
            <div>
              <label className="block font-medium mb-2">
                Email, username <span className="text-red-600">*</span>
              </label>
              <input
                type="text"
                value={emailOrUsername}
                onChange={(e) => setEmailOrUserName(e.target.value)}
                className="w-full h-12 border rounded-[10px] px-3 py-2 hover:outline outline-auto duration-85 ease-in-out"
                placeholder="Enter email or username"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block font-medium mb-2">
                Password <span className="text-red-600">*</span>
              </label>
              <ShowHidePassword
                placeholder="Password"
                value={password}
                onChange={(e: any) => setPassword(e.target.value)}
              />
            </div>

            {/* Forgot password */}
            <div>
              <Link
                to="/forgotpassword"
                className="flex justify-end font-medium underline mt-8"
              >
                Forgot password?
              </Link>
            </div>

            {/* Sign in Button */}
            <div>
              <button className="w-full h-12 font-semibold rounded-[10px] bg-[#8F87F1] text-white hover:bg-[#A555EC] cursor-pointer duration-85 ease-in-out">
                SIGN IN
              </button>
            </div>
          </form>
        )}

        {/* Sign up Form */}
        {tab === "signup" && (
          <form className="space-y-4 duration-75 ease-in-out">
            {/* Name */}
            <label className="block font-medium mb-2">
              Name (Last, first) <span className="text-red-600">*</span>
            </label>
            <input
              type="text"
              className="w-full h-12 border rounded-[10px] px-3 py-2 hover:outline outline-auto duration-85 ease-in-out"
              placeholder="Name"
            />

            {/* Birthday */}
            <label className="block font-medium mb-2">
              Birthday <span className="text-red-600">*</span>
            </label>
            <Calendar />

            {/* Email */}
            <label className="block font-medium mb-2">
              Email <span className="text-red-600">*</span>
            </label>
            <input
              type="text"
              className="w-full h-12 border rounded-[10px] px-3 py-2 hover:outline outline-auto duration-85 ease-in-out"
              placeholder="Email"
            />

            {/* Username */}
            <label className="block font-medium mb-2">
              Username <span className="text-red-600">*</span>
            </label>
            <input
              type="text"
              className="w-full h-12 border rounded-[10px] px-3 py-2 hover:outline outline-auto duration-85 ease-in-out"
              placeholder="Username"
            />

            {/* Password */}
            <label className="block font-medium mb-2">
              Password <span className="text-red-600">*</span>
            </label>
            <ShowHidePassword
              placeholder="Password"
              value={password}
              onChange={(e: any) => setPassword(e.target.value)}
            />

            {/* Confirm password */}
            <label className="block font-medium mb-2">
              Confirm password <span className="text-red-600">*</span>
            </label>
            <ShowHidePassword
              placeholder="Confirm password"
              value={password}
              onChange={(e: any) => setPassword(e.target.value)}
            />

            {/* Sign up Button */}
            <button className="w-full h-12 font-semibold text-white border rounded-[10px] mt-8 bg-[#8F87F1] hover:bg-[#A555EC] cursor-pointer duration-85 ease-in-out">
              SIGN UP
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
