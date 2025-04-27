import { useEffect, useState } from "react";
import io from "socket.io-client";

const ws = io(import.meta.env.VITE_API_URL.replace("/api","/ws"));

export default function AlertToast() {
  const [alert, setAlert] = useState(null);

  useEffect(() => {
    ws.on("alert_new", setAlert);
    return () => ws.disconnect();
  }, []);

  if (!alert) return null;

  return (
    <div className="fixed bottom-4 right-4 bg-cove-alert text-white p-4 rounded shadow-lg">
      <strong>{alert.alert_type}</strong><br />
      {alert.description}
    </div>
  );
}
