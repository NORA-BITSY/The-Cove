import React, { useState, useEffect } from "react";

export default function OnboardingModal() {
  const [show, setShow] = useState(false);

  useEffect(() => {
    const hasSeen = localStorage.getItem("hasSeenOnboarding");
    if (!hasSeen) {
      setShow(true);
      localStorage.setItem("hasSeenOnboarding", "true");
    }
  }, []);

  if (!show) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 max-w-md w-full rounded shadow-lg">
        <h2 className="text-xl font-bold mb-4">Welcome Aboard!</h2>
        <p className="mb-4">
          Thank you for joining The Cove. Let’s get you started:
        </p>
        <ul className="list-disc list-inside mb-4">
          <li>Claim a spot on the sandbar using the interactive map.</li>
          <li>Check out upcoming events in the calendar.</li>
          <li>Watch or start a live stream.</li>
          <li>Post a global message or chat with other boaters!</li>
        </ul>
        <button className="btn" onClick={() => setShow(false)}>Got it!</button>
      </div>
    </div>
  );
}
