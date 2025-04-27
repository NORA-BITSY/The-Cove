import React, { useEffect, useState, useContext } from "react";
import { AuthCtx } from "../context/AuthContext";

export default function BadgesPage() {
  const { jwt } = useContext(AuthCtx);
  const [badges, setBadges] = useState([]);

  useEffect(() => {
    if (jwt) {
      fetch("/api/badges", { headers: { Authorization: `Bearer ${jwt}` } })
        .then(r => r.json())
        .then(data => setBadges(data.badges || []));
    }
  }, [jwt]);

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">My Badges</h2>
      <ul className="list-disc list-inside">
        {badges.map((b, idx) => (
          <li key={idx}>{b}</li>
        ))}
      </ul>
    </div>
  );
}
