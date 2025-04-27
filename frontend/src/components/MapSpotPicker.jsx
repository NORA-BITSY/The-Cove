import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { fetchSpots, claimSpot } from "../api";
import io from "socket.io-client";

const ws = io(import.meta.env.VITE_API_URL.replace("/api", "/ws"));

export default function MapSpotPicker() {
  const [spots, setSpots] = useState([]);

  useEffect(() => {
    fetchSpots().then(setSpots);
    ws.on("spot_update", () => {
      fetchSpots().then(setSpots);
    });
    return () => ws.disconnect();
  }, []);

  const handleClaim = async (id) => {
    const note = prompt("Optional note?");
    await claimSpot(id, note || "", localStorage.getItem("jwt"));
    setSpots(await fetchSpots());
  };

  return (
    <section>
      <h2 className="text-xl font-bold mb-2">Reserve a Spot</h2>
      <MapContainer
        center={[44.6337, -92.6207]}
        zoom={15}
        scrollWheelZoom
        className="h-80 w-full rounded"
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {spots.map((s) => (
          <Marker key={s.id} position={[s.lat, s.lon]}>
            <Popup>
              {s.claimant_id ? (
                <>
                  <b>Claimed</b>
                  <br />
                  Note: {s.note || "—"}
                </>
              ) : (
                <button onClick={() => handleClaim(s.id)} className="btn">
                  Claim this spot
                </button>
              )}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </section>
  );
}
