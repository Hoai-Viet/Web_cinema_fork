import { createContext, useState, useContext, useEffect } from "react";
import type { ReactNode } from "react";

interface AuthContextType {
  user: string | null;
  token: string | null;
  login: (username: string, token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  login: () => {},
  logout: () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);

  // 🔹 Khôi phục từ localStorage khi reload trang
  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    const storedToken = localStorage.getItem("token");
    if (storedUser) setUser(storedUser);
    if (storedToken) setToken(storedToken);
  }, []);

  // 🔹 Khi login thành công
  const login = (username: string, tokenValue: string) => {
    setUser(username);
    setToken(tokenValue);
    localStorage.setItem("user", username);
    localStorage.setItem("token", tokenValue);
  };

  // 🔹 Khi logout
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

export const useAuth = () => useContext(AuthContext);
