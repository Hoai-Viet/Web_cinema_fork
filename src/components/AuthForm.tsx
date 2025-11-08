import { useState } from "react";
import ShowHidePassword from "./ShowHidePassword";
import Calendar from "./Calendar";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function AuthForm() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [tab, setTab] = useState<"signin" | "signup">("signin");

  const [emailOrUsername, setEmailOrUserName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<{ user?: string; pass?: string }>({});
  const [signupError, setSignupError] = useState<Record<string, string>>({});

  const [signupData, setSignupData] = useState({
    name: "",
    birthday: "",
    email: "",
    username: "",
    password: "",
    confirmPassword: "",
  });

  // -------------------- LOGIN --------------------
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError({});

    if (!emailOrUsername || !password) {
      setError({
        user: !emailOrUsername
          ? "Please enter your email or username"
          : undefined,
        pass: !password ? "Please enter your password" : undefined,
      });
      return;
    }

    try {
      const res = await fetch("http://localhost:5000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: emailOrUsername,
          password: password,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        if (data.message?.includes("password")) {
          setError({ pass: "Incorrect password" });
        } else if (
          data.message?.includes("username") ||
          data.message?.includes("email")
        ) {
          setError({ user: "Incorrect username or email" });
        } else {
          setError({ user: "Invalid login credentials" });
        }
        return;
      }

      login(data.user.username, data.access_token);
      localStorage.setItem("token", data.access_token);
      navigate("/");
    } catch {
      setError({ user: "Network error, please try again later" });
    }
  };

  // -------------------- SIGNUP --------------------
  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setSignupError({});

    const err: Record<string, string> = {};
    const { name, birthday, email, username, password, confirmPassword } =
      signupData;

    // 1. Kiểm tra trường trống
    if (!name) err.name = "Please enter your name";
    if (!birthday) err.birthday = "Please select your birthday";
    if (!email) err.email = "Please enter your email";
    if (!username) err.username = "Please enter your username";
    if (!password) err.password = "Please enter your password";
    if (!confirmPassword) err.confirmPassword = "Please confirm your password";

    // 2. Kiểm tra tuổi ≥ 12
    if (birthday) {
      const birthDate = new Date(birthday);
      const today = new Date();
      const age =
        today.getFullYear() -
        birthDate.getFullYear() -
        (today <
        new Date(today.getFullYear(), birthDate.getMonth(), birthDate.getDate())
          ? 1
          : 0);
      if (age < 12) err.birthday = "You must be at least 12 years old";
    }

    // 3. Kiểm tra độ dài mật khẩu
    if (password && password.length < 8)
      err.password = "Password must be at least 8 characters";

    // 4. Kiểm tra xác nhận mật khẩu
    if (password && confirmPassword && password !== confirmPassword)
      err.confirmPassword = "Passwords do not match";

    if (Object.keys(err).length > 0) {
      setSignupError(err);
      return;
    }

    try {
      const res = await fetch("http://localhost:5000/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          birthday,
          email,
          username,
          password,
          confirm_password: confirmPassword,
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        alert(data.message || "Signup failed");
        return;
      }

      alert("Account created successfully!");
      setTab("signin");
    } catch {
      alert("Network error, please try again later");
    }
  };

  return (
    <div className="w-full px-40">
      <div className="bg-white border-3 border-[#D0A2F7] rounded-[10px] p-8 w-[450px] my-12">
        {/* Tab */}
        <div className="flex justify-center mb-6 gap-18">
          <button
            onClick={() => setTab("signin")}
            className={`px-6 py-2 h-14 w-38 rounded-[10px] font-semibold ${
              tab === "signin"
                ? "bg-[#8F87F1] text-white"
                : "hover:bg-[#F5F5F0] cursor-pointer"
            }`}
          >
            SIGN IN
          </button>
          <button
            onClick={() => setTab("signup")}
            className={`px-6 py-2 h-14 w-38 rounded-[10px] font-semibold ${
              tab === "signup"
                ? "bg-[#8F87F1] text-white"
                : "hover:bg-[#F5F5F0] cursor-pointer"
            }`}
          >
            SIGN UP
          </button>
        </div>

        {/* Sign in form */}
        {tab === "signin" && (
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block font-medium mb-2">
                Email, username <span className="text-red-600">*</span>
              </label>
              <input
                type="text"
                value={emailOrUsername}
                onChange={(e) => setEmailOrUserName(e.target.value)}
                className="w-full h-12 border rounded-[10px] px-3 py-2"
                placeholder="Enter email or username"
              />
              {error.user && (
                <p className="text-red-600 text-sm mt-1">{error.user}</p>
              )}
            </div>

            <div>
              <label className="block font-medium mb-2">
                Password <span className="text-red-600">*</span>
              </label>
              <ShowHidePassword
                placeholder="Password"
                value={password}
                onChange={(e: any) => setPassword(e.target.value)}
              />
              {error.pass && (
                <p className="text-red-600 text-sm mt-1">{error.pass}</p>
              )}
            </div>

            <div>
              <Link
                to="/forgotpassword"
                className="flex justify-end font-medium underline mt-8"
              >
                Forgot password?
              </Link>
            </div>

            <div>
              <button
                type="submit"
                className="w-full h-12 font-semibold rounded-[10px] bg-[#8F87F1] text-white hover:bg-[#A555EC]"
              >
                SIGN IN
              </button>
            </div>
          </form>
        )}

        {/* Sign up form */}
        {tab === "signup" && (
          <form onSubmit={handleSignup} className="space-y-4">
            <div>
              <label className="block font-medium mb-2">
                Name (Last, first) <span className="text-red-600">*</span>
              </label>
              <input
                type="text"
                className="w-full h-12 border rounded-[10px] px-3 py-2"
                placeholder="Name"
                value={signupData.name}
                onChange={(e) =>
                  setSignupData({ ...signupData, name: e.target.value })
                }
              />
              {signupError.name && (
                <p className="text-red-600 text-sm mt-1">{signupError.name}</p>
              )}
            </div>

            <div>
              <label className="block font-medium mb-2">
                Birthday <span className="text-red-600">*</span>
              </label>
              <Calendar
                onChange={(date: string) =>
                  setSignupData({ ...signupData, birthday: date })
                }
              />
              {signupError.birthday && (
                <p className="text-red-600 text-sm mt-1">
                  {signupError.birthday}
                </p>
              )}
            </div>

            <div>
              <label className="block font-medium mb-2">
                Email <span className="text-red-600">*</span>
              </label>
              <input
                type="text"
                className="w-full h-12 border rounded-[10px] px-3 py-2"
                placeholder="Email"
                value={signupData.email}
                onChange={(e) =>
                  setSignupData({ ...signupData, email: e.target.value })
                }
              />
              {signupError.email && (
                <p className="text-red-600 text-sm mt-1">{signupError.email}</p>
              )}
            </div>

            <div>
              <label className="block font-medium mb-2">
                Username <span className="text-red-600">*</span>
              </label>
              <input
                type="text"
                className="w-full h-12 border rounded-[10px] px-3 py-2"
                placeholder="Username"
                value={signupData.username}
                onChange={(e) =>
                  setSignupData({ ...signupData, username: e.target.value })
                }
              />
              {signupError.username && (
                <p className="text-red-600 text-sm mt-1">
                  {signupError.username}
                </p>
              )}
            </div>

            <div>
              <label className="block font-medium mb-2">
                Password <span className="text-red-600">*</span>
              </label>
              <ShowHidePassword
                placeholder="Password"
                value={signupData.password}
                onChange={(e) =>
                  setSignupData({ ...signupData, password: e.target.value })
                }
              />
              {signupError.password && (
                <p className="text-red-600 text-sm mt-1">
                  {signupError.password}
                </p>
              )}
            </div>

            <div>
              <label className="block font-medium mb-2">
                Confirm password <span className="text-red-600">*</span>
              </label>
              <ShowHidePassword
                placeholder="Confirm password"
                value={signupData.confirmPassword}
                onChange={(e) =>
                  setSignupData({
                    ...signupData,
                    confirmPassword: e.target.value,
                  })
                }
              />
              {signupError.confirmPassword && (
                <p className="text-red-600 text-sm mt-1">
                  {signupError.confirmPassword}
                </p>
              )}
            </div>

            <button
              type="submit"
              className="w-full h-12 font-semibold text-white border rounded-[10px] mt-8 bg-[#8F87F1] hover:bg-[#A555EC]"
            >
              SIGN UP
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
