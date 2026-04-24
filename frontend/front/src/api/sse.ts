// src/api/sse.ts
export function createSSE(url: string, onMessage: (data: any) => void) {
  const eventSource = new EventSource(url);

  eventSource.onmessage = (event) => {
    onMessage(event.data);
  };

  eventSource.onerror = () => {
    eventSource.close();
  };

  return eventSource;
}