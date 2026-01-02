import Image from "next/image";
import SponsorshipCheck from "./components/SponsorshipCheck";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start text-center sm:text-left">
        <h1 className="text-4xl font-bold text-center w-full text-blue-900">
          UK Visa Jobs Platform
        </h1>
        <p className="text-lg text-gray-600 text-center w-full max-w-2xl">
          Find UK jobs that strictly offer visa sponsorship. Verified against the official Gov.uk register.
        </p>

        <div className="w-full">
          <SponsorshipCheck />
        </div>
      </main>

      <footer className="mt-20 text-gray-400 text-sm">
        <p>Data Source: GOV.UK Register of Licensed Sponsors</p>
      </footer>
    </div>
  );
}
