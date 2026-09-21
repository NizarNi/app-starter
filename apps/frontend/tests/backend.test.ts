// @vitest-environment node

import { getBackendHealth } from "@/lib/backend";

describe("getBackendHealth", () => {
  const fetchMock = vi.fn<typeof fetch>();

  beforeEach(() => {
    vi.useFakeTimers();
    vi.stubEnv("BACKEND_URL", "http://backend.test:8000");
    vi.stubGlobal("fetch", fetchMock);
  });

  afterEach(() => {
    const remainingTimers = vi.getTimerCount();
    vi.clearAllTimers();
    vi.useRealTimers();
    vi.unstubAllGlobals();
    vi.unstubAllEnvs();
    fetchMock.mockReset();
    expect(remainingTimers).toBe(0);
  });

  it("requests the configured backend and returns its healthy status", async () => {
    fetchMock.mockResolvedValue(Response.json({ status: "ok", service: "backend" }));

    await expect(getBackendHealth()).resolves.toEqual({ available: true, status: "ok" });
    expect(fetchMock).toHaveBeenCalledWith(new URL("http://backend.test:8000/health"), {
      cache: "no-store",
      signal: expect.any(AbortSignal)
    });
  });

  it.each([404, 500, 503])("returns unavailable for HTTP %i", async (status) => {
    fetchMock.mockResolvedValue(
      Response.json({ status: "ok", service: "backend" }, { status })
    );

    await expect(getBackendHealth()).resolves.toEqual({ available: false });
  });

  it.each([
    null,
    [],
    "ok",
    {},
    { status: 123, service: "backend" },
    { status: "error", service: "backend" },
    { status: "ok" },
    { status: "ok", service: "another-service" }
  ])("returns unavailable for an invalid payload: %j", async (payload) => {
    fetchMock.mockResolvedValue(Response.json(payload));

    await expect(getBackendHealth()).resolves.toEqual({ available: false });
  });

  it("returns unavailable for malformed JSON", async () => {
    fetchMock.mockResolvedValue(new Response("not JSON"));

    await expect(getBackendHealth()).resolves.toEqual({ available: false });
  });

  it("returns unavailable for a network failure", async () => {
    fetchMock.mockRejectedValue(new TypeError("fetch failed"));

    await expect(getBackendHealth()).resolves.toEqual({ available: false });
  });

  it("aborts a stalled request after two seconds and returns unavailable", async () => {
    let requestSignal: AbortSignal | undefined;
    fetchMock.mockImplementation((_url, init) => {
      requestSignal = init?.signal ?? undefined;
      return new Promise((_resolve, reject) => {
        requestSignal?.addEventListener("abort", () => reject(requestSignal?.reason), {
          once: true
        });
      });
    });

    const result = getBackendHealth();
    await vi.advanceTimersByTimeAsync(1_999);
    expect(requestSignal?.aborted).toBe(false);
    await vi.advanceTimersByTimeAsync(1);

    await expect(result).resolves.toEqual({ available: false });
    expect(requestSignal?.aborted).toBe(true);
  });

  it("keeps the same deadline while reading a stalled response body", async () => {
    let requestSignal: AbortSignal | undefined;
    fetchMock.mockImplementation((_url, init) => {
      requestSignal = init?.signal ?? undefined;
      const body = new ReadableStream({
        start(controller) {
          controller.enqueue(new TextEncoder().encode('{"status":'));
          requestSignal?.addEventListener("abort", () => controller.error(requestSignal?.reason), {
            once: true
          });
        }
      });
      // Headers arrive partway through the deadline, but the body never finishes.
      return new Promise((resolve) => {
        setTimeout(() => resolve(new Response(body)), 1_000);
      });
    });

    const result = getBackendHealth();
    await vi.advanceTimersByTimeAsync(1_999);
    expect(requestSignal?.aborted).toBe(false);
    await vi.advanceTimersByTimeAsync(1);

    await expect(result).resolves.toEqual({ available: false });
    expect(requestSignal?.aborted).toBe(true);
  });
});
