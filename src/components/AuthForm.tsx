import { useState } from "react";
import ShowHidePassword from "./ShowHidePassword";

export default function AuthForm() {
  const [tab, setTab] = useState<"signin" | "signup">("signin");

  return (
    <div className="flex justify-start items-center px-38 py-14 bg-[#FDFCF0]">
      <div className="bg-white border rounded-[10px] p-8 w-[600px] ">
        {/* Tab */}
        <div className="flex justify-center mb-6 gap-20">
          <button
            onClick={() => setTab("signin")}
            className={`px-6 py-2 h-14 w-38 rounded-[10px] font-semibold duration-75 ease-in-out  ${
              tab === "signin"
                ? "bg-[#FFE507] border border-black"
                : "hover:bg-[#F5F5F0] cursor-pointer duration-150 ease-in-out"
            }`}
          >
            SIGN IN
          </button>
          <button
            onClick={() => setTab("signup")}
            className={`px-6 py-2 h-14 w-38 rounded-[10px] font-semibold duration-75 ease-in-out  ${
              tab === "signup"
                ? "bg-[#FFE507] border border-black"
                : "hover:bg-[#F5F5F0] cursor-pointer duration-150 ease-in-out"
            }`}
          >
            SIGN UP
          </button>
        </div>

        {/* Sign in Form */}
        <form className="space-y-4">
          {/* Username, email box */}
          <div>
            <label className="block font-medium mb-2">
              Email, username <span className="text-red-600">*</span>
            </label>
            <input
              type="text"
              className="w-full h-12 border border-black rounded-[10px] px-3 py-2"
              placeholder="Enter email or username"
            />
          </div>

          {/* Password */}
          <div>
            <label className="block font-medium mb-2">
              Password <span className="text-red-600">*</span>
            </label>
            <ShowHidePassword />
          </div>

          {/* Forgot password */}
          <div>
            <a href="#" className="flex justify-end font-medium underline mt-8">
              Forgot password?
            </a>
          </div>

          {/* Sign in Button */}
          <div>
            <button className="w-full h-12 font-semibold border border-black rounded-[10px] bg-[#FFE99A] hover:bg-[#FFD586] cursor-pointer duration-75 ease-in-out">
              SIGN IN
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
