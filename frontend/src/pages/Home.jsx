import React from "react";
import LiveStream from "../components/LiveStream";
import MapSpotPicker from "../components/MapSpotPicker";
import GlobalMessageFeed from "../components/GlobalMessageFeed";
import OnboardingModal from "../components/OnboardingModal";

export default function Home() {
  return (
    <main className="max-w-6xl mx-auto p-4">
      <OnboardingModal />
      <h1 className="text-3xl font-bold mb-4">Welcome to The Cove</h1>
      <div className="mb-6">
        <GlobalMessageFeed />
      </div>
      <div className="grid lg:grid-cols-2 gap-6">
        <LiveStream />
        <MapSpotPicker />
      </div>
    </main>
  );
}
