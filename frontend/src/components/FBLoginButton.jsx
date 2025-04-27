import FacebookLogin from "react-facebook-login-lite";
import { useContext } from "react";
import { AuthCtx } from "../context/AuthContext";
import { API } from "../api";

export default function FBLoginButton() {
  const { save } = useContext(AuthCtx);

  const handle = async (fbData) => {
    const res = await fetch(`${API}/auth/facebook`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ access_token: fbData.accessToken }),
    });
    const data = await res.json();
    save(data.access_token);
  };

  return (
    <FacebookLogin
      appId={import.meta.env.VITE_FB_APP_ID}   // <-- UPDATED
      onSuccess={handle}
      render={({ onClick }) => (
        <button onClick={onClick} className="btn">
          Login with Facebook
        </button>
      )}
    />
  );
}
