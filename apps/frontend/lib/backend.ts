import type { BackendHealthState } from "@/components/BackendHealth";

export async function getBackendHealth(): Promise<BackendHealthState> {
  const backendUrl = process.env.BACKEND_URL ?? "http://backend:8000";
  const controller = new AbortController();
  // Keep the deadline active until the response body has also been read.
  const timeout = setTimeout(() => controller.abort(), 2_000);

  try {
    const response = await fetch(new URL("/health", backendUrl), {
      cache: "no-store",
      signal: controller.signal
    });

    if (!response.ok) {
      return { available: false };
    }

    const payload: unknown = await response.json();

    if (
      typeof payload !== "object" ||
      payload === null ||
      !("status" in payload) ||
      payload.status !== "ok" ||
      !("service" in payload) ||
      payload.service !== "backend"
    ) {
      return { available: false };
    }

    return { available: true, status: payload.status };
  } catch {
    return { available: false };
  } finally {
    clearTimeout(timeout);
  }
}
