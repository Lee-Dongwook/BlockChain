export const ws = new WebSocket(
  import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws"
);

ws.onopen = () => console.log("[WS] Connected");
ws.onmessage = (msg) => console.log("[WS] Message", msg.data);
ws.onclose = () => console.log("[WS] Disconnected");
