import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function PlayerSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  async function handleSearch() {
    const res = await fetch(`http://localhost:8000/players/search?q=${query}`);
    const data = await res.json();
    setResults(data);
  }

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search players..."
      />
      <button onClick={handleSearch}>Search</button>

      <ul>
        {results.map((p) => (
          <li
            key={p.espn_id}
            onClick={() => navigate(`/player/${p.espn_id}`)}
            style={{ cursor: "pointer" }}
          >
            {p.full_name}
          </li>
        ))}
      </ul>
    </div>
  );
}
