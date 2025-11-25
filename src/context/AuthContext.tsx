import { createContext, useState, useContext, useEffect } from "react";
import type { ReactNode } from "react";

// =========================
// 1. Định nghĩa kiểu User
// =========================
interface User {
  id: number;
  username: string;
}

// =========================
// 2. Kiểu của AuthContext
// =========================
interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (userObj: User, token: string) => void;
  logout: () => void;
}

// =========================
// 3. Tạo context
// =========================
const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  login: () => {},
  logout: () => {},
});

// =========================
// 4. Provider
// =========================
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  // Load lại từ localStorage khi reload trang
  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    const storedToken = localStorage.getItem("token");

    if (storedUser) setUser(JSON.parse(storedUser));
    if (storedToken) setToken(storedToken);
  }, []);

  // Login: backend trả về user_id + username → FE gọi login()
  const login = (userObj: User, tokenValue: string) => {
    setUser(userObj);
    setToken(tokenValue);

    localStorage.setItem("user", JSON.stringify(userObj));
    localStorage.setItem("token", tokenValue);
  };

  // Logout
  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("user");
    localStorage.removeItem("token");
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook lấy user
export const useAuth = () => useContext(AuthContext);
