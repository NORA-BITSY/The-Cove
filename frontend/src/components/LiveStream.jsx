import React, { useState, useEffect, useRef, useContext } from "react";
import { AuthCtx } from "../context/AuthContext";
import io from "socket.io-client";
import { fetchActiveStreams, startStream } from "../api";

const ws = io(import.meta.env.VITE_API_URL.replace("/api", "/ws"), {
  auth: { token: localStorage.getItem("jwt") },
});
const MEDIA_WS_URL = import.meta.env.VITE_MEDIA_WS || "ws://localhost:3333";

export default function LiveStream() {
  const { jwt } = useContext(AuthCtx);
  const [streams, setStreams] = useState([]);
  const [streaming, setStreaming] = useState(false);
  const [watching, setWatching] = useState(null);
  const [messages, setMessages] = useState([]);
  const [viewers, setViewers] = useState(0);
  const localVideoRef = useRef(null);
  const remoteVideoRef = useRef(null);
  const pcRef = useRef(null);
  const wsStreamRef = useRef(null);
  const streamIdRef = useRef(null);
  const messageInputRef = useRef(null);

  useEffect(() => {
    fetchActiveStreams().then(setStreams);
    ws.on("stream_started", (stream) => {
      setStreams((prev) => [...prev, stream]);
    });
    ws.on("stream_stopped", ({ stream_id }) => {
      setStreams((prev) => prev.filter((s) => s.id !== stream_id));
      if (watching === stream_id) stopWatching();
    });
    ws.on("chat_message", (msg) => {
      setMessages((prev) => [...prev, `${msg.user}: ${msg.message}`]);
    });
    ws.on("viewer_count", setViewers);
    return () => ws.off("viewer_count", setViewers);
  }, []);

  const startPublishing = async (streamId) => {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true,
    });
    localVideoRef.current.srcObject = stream;
    const pc = new RTCPeerConnection();
    pcRef.current = pc;
    stream.getTracks().forEach((track) => pc.addTrack(track, stream));
    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);
    const wsStream = new WebSocket(`${MEDIA_WS_URL}/app/cove/${streamId}`);
    wsStreamRef.current = wsStream;
    wsStream.onopen = () => {
      wsStream.send(JSON.stringify({ command: "publish", sdp: pc.localDescription }));
    };
    wsStream.onmessage = async (event) => {
      const msg = JSON.parse(event.data);
      if (msg.command === "answer") {
        await pc.setRemoteDescription(msg.sdp);
      } else if (msg.command === "candidate") {
        await pc.addIceCandidate(msg.candidate);
      }
    };
    pc.onicecandidate = (event) => {
      if (event.candidate) {
        wsStream.send(JSON.stringify({ command: "candidate", candidate: event.candidate }));
      }
    };
  };

  const startWatching = async (streamId) => {
    const pc = new RTCPeerConnection();
    pcRef.current = pc;
    pc.ontrack = (event) => {
      remoteVideoRef.current.srcObject = event.streams[0];
    };
    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);
    const wsStream = new WebSocket(`${MEDIA_WS_URL}/app/cove/${streamId}`);
    wsStreamRef.current = wsStream;
    wsStream.onopen = () => {
      wsStream.send(JSON.stringify({ command: "play", sdp: pc.localDescription }));
    };
    wsStream.onmessage = async (event) => {
      const msg = JSON.parse(event.data);
      if (msg.command === "answer") {
        await pc.setRemoteDescription(msg.sdp);
      } else if (msg.command === "candidate") {
        await pc.addIceCandidate(msg.candidate);
      }
    };
    pc.onicecandidate = (event) => {
      if (event.candidate) {
        wsStream.send(JSON.stringify({ command: "candidate", candidate: event.candidate }));
      }
    };
    ws.emit("join_stream", { stream_id: streamId });
    setWatching(streamId);
  };

  const stopWatching = () => {
    if (pcRef.current) pcRef.current.close();
    if (wsStreamRef.current) wsStreamRef.current.close();
    setWatching(null);
    setMessages([]);
    remoteVideoRef.current.srcObject = null;
  };

  const handleStartStream = async () => {
    const title = prompt("Enter stream title");
    if (title) {
      const streamId = await startStream(title, jwt);
      streamIdRef.current = streamId;
      await startPublishing(streamId);
      setStreaming(true);
      ws.emit("join_stream", { stream_id: streamId });
    }
  };

  const handleStopStream = () => {
    if (pcRef.current) pcRef.current.close();
    if (wsStreamRef.current) wsStreamRef.current.close();
    setStreaming(false);
    localVideoRef.current.srcObject = null;
  };

  const sendMessage = () => {
    const message = messageInputRef.current.value;
    if (message && watching) {
      ws.emit("chat_message", { stream_id: watching, message });
      messageInputRef.current.value = "";
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Live Streams</h2>
      <div className="grid gap-2">
        {streams.map((stream) => (
          <div key={stream.id} className="flex items-center space-x-2">
            <p>{stream.title} by {stream.streamer_name}</p>
            <button
              onClick={() => startWatching(stream.id)}
              className="btn"
              disabled={streaming || watching === stream.id}
            >
              Watch
            </button>
          </div>
        ))}
      </div>
      {jwt && !streaming && !watching && (
        <button onClick={handleStartStream} className="btn">
          Start My Stream
        </button>
      )}
      {streaming && (
        <div>
          <video ref={localVideoRef} autoPlay muted className="w-full max-w-md rounded" />
          <button onClick={handleStopStream} className="btn btn-danger mt-2">
            Stop Streaming
          </button>
        </div>
      )}
      {watching && (
        <div>
          <video ref={remoteVideoRef} autoPlay className="w-full max-w-md rounded" />
          <button onClick={stopWatching} className="btn btn-danger mt-2">
            Stop Watching
          </button>
          <div className="mt-4">
            <h3 className="font-semibold">Chat</h3>
            <div className="h-40 overflow-y-auto border p-2 rounded">
              {messages.map((msg, i) => (
                <p key={i}>{msg}</p>
              ))}
            </div>
            <div className="flex mt-2">
              <input
                ref={messageInputRef}
                type="text"
                className="flex-1 border rounded px-2"
                placeholder="Type a message..."
              />
              <button onClick={sendMessage} className="btn ml-2">
                Send
              </button>
            </div>
          </div>
        </div>
      )}
      <p className="mt-2">Live viewers: <b>{viewers}</b></p>
    </div>
  );
}
