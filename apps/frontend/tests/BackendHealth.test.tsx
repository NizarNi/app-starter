import { render, screen } from "@testing-library/react";

import { BackendHealth } from "@/components/BackendHealth";

describe("BackendHealth", () => {
  it("shows a connected backend", () => {
    render(<BackendHealth health={{ available: true, status: "ok" }} />);

    expect(screen.getByRole("status")).toHaveTextContent("Backend status: connected (ok)");
  });

  it("shows when the backend cannot be reached", () => {
    render(<BackendHealth health={{ available: false }} />);

    expect(screen.getByRole("status")).toHaveTextContent("Backend status: unavailable");
  });
});
