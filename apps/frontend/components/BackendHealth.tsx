export type BackendHealthState = {
  available: boolean;
  status?: string;
};

type BackendHealthProps = {
  health: BackendHealthState;
};

export function BackendHealth({ health }: BackendHealthProps) {
  if (health.available) {
    return (
      <p className="health" data-status="available" role="status">
        Backend status: connected ({health.status ?? "ok"})
      </p>
    );
  }

  return (
    <p className="health" data-status="unavailable" role="status">
      Backend status: unavailable
    </p>
  );
}
