import { createContext, useState } from "react";
export const AuthCtx = createContext(null);

export default function AuthProvider({ children }) {
  const [jwt, setJwt] = useState(localStorage.getItem("jwt"));

  const save = (token) => {
    localStorage.setItem("jwt", token);
    setJwt(token);
  };

  const logout = () => {
    localStorage.removeItem("jwt");
    setJwt(null);
  };

  return (
    <AuthCtx.Provider value={{ jwt, save, logout }}>
      {children}
    </AuthCtx.Provider>
  );
}
