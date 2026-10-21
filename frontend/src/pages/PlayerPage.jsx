import { useParams } from "react-router-dom";
import usePlayer from "../hooks/usePlayer";
import PlayerCard from "../components/PlayerCard";

export default function PlayerPage() {
  const { id } = useParams();
  const player = usePlayer(id);

  return (
    <div className="flex justify-center p-10">
      <PlayerCard player={player} />
    </div>
  );
}
