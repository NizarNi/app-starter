import { BackendHealth } from "@/components/BackendHealth";
import { getBackendHealth } from "@/lib/backend";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const backendHealth = await getBackendHealth();

  return (
    <main>
      <section className="landing-card" aria-labelledby="page-title">
        <p>Application starter</p>
        <h1 id="page-title">App Starter</h1>
        <p>
          The application foundation is running.
        </p>
        <BackendHealth health={backendHealth} />
      </section>
    </main>
  );
}
