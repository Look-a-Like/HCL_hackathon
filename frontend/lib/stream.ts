import type { AgentEvent } from "./types";

export async function* streamPlan(query: string): AsyncGenerator<AgentEvent> {
  const res = await fetch("/api/plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  if (!res.ok || !res.body) {
    const text = await res.text().catch(() => "Unknown error");
    yield { type: "error", error: text };
    return;
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      const raw = line.slice(6).trim();
      if (!raw || raw === "[DONE]") continue;
      try {
        yield JSON.parse(raw) as AgentEvent;
      } catch {
        // malformed line — skip
      }
    }
  }
}
