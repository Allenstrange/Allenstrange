"use client";
import { useState } from 'react';

export default function SponsorshipCheck() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const checkSponsor = async () => {
    if (!query) return;
    setLoading(true);
    setResult(null);
    try {
      // Using 127.0.0.1 for better compatibility in some local envs
      const url = `http://127.0.0.1:8000/employers/verify?name=${encodeURIComponent(query)}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error("Network response was not ok");
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error("Fetch error:", e);
      setResult({ error: "Failed to fetch. Ensure backend is running." });
    }
    setLoading(false);
  };

  return (
    <div className="p-4 border rounded shadow-sm bg-white max-w-md mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Check Employer Sponsorship</h2>
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Company Name (e.g. BBC)"
          className="border p-2 flex-grow rounded text-gray-800"
          onKeyDown={(e) => e.key === 'Enter' && checkSponsor()}
        />
        <button
          onClick={checkSponsor}
          className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50 hover:bg-blue-700 transition"
          disabled={loading}
        >
          {loading ? '...' : 'Check'}
        </button>
      </div>

      {result && (
        <div className="mt-4">
            {result.error ? (
                 <div className="p-3 bg-yellow-100 border-yellow-400 text-yellow-700 rounded">
                    <strong>⚠️ Error</strong>
                    <p className="text-sm">{result.error}</p>
                 </div>
            ) : result.verified ? (
                <div className="p-3 bg-green-100 border-green-400 text-green-700 rounded">
                    <strong>✅ Verified Sponsor</strong>
                    <p className="text-sm mt-1">Found {result.matches.length} match(es).</p>
                    <ul className="list-disc pl-5 mt-2 text-sm">
                        {result.matches.map((m: any) => (
                            <li key={m.id}>
                                {m.organisation_name} <span className='text-gray-500'>({m.town_city})</span>
                            </li>
                        ))}
                    </ul>
                </div>
            ) : (
                <div className="p-3 bg-red-100 border-red-400 text-red-700 rounded">
                    <strong>❌ Not Verified</strong>
                    <p className="text-sm">No exact match found for "{result.query}".</p>
                </div>
            )}
        </div>
      )}
    </div>
  );
}
