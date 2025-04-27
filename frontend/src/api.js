export const API = import.meta.env.VITE_API_URL || "https://thecove.boatable.app/api";

export async function fetchSpots() {
  const res = await fetch(`${API}/spots`);
  return res.json();
}

export async function claimSpot(id, note, token) {
  const res = await fetch(`${API}/spots/${id}/claim?note=${note}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

export async function fetchActiveStreams() {
  const res = await fetch(`${API}/streams`);
  return res.json();
}

export async function startStream(title, token) {
  const res = await fetch(`${API}/streams`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ title }),
  });
  return (await res.json()).id;
}
