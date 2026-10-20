import { useEffect, useState } from "react";

export default function usePlayer(id) {
  const [player, setPlayer] = useState(null);

  useEffect(() => {
    if (!id) return;

    fetch(`http://localhost:8000/players/${id}/full`)
      .then(res => res.json())
      .then(data => setPlayer(data));
  }, [id]);

  return player;
}
