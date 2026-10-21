export default function PlayerCard({ player }) {
  console.log("PLAYER DATA:", player);

  
    if (!player) return null;

    const { details, stats } = player;

    const {
        full_name,
        headshot,
        team,
        position,
        age,
        height,
        weight,
        draft
    } = details;

  return (
    <div className="text-white p-6 max-w-3xl mx-auto">
      <div className="flex items-center gap-6">
        <img
          src={headshot}
          alt={full_name}
          className="w-32 h-32 rounded-lg object-cover border border-gray-700"
        />

        <div>
          <h1 className="text-3xl font-bold">{full_name}</h1>
          <p className="text-gray-300">{position}</p>
          <p className="text-gray-400">Team: {team || "N/A"}</p>
          <p className="text-gray-400">Age: {age || "N/A"}</p>
          <p className="text-gray-400">Height: {height}</p>
          <p className="text-gray-400">Weight: {weight}</p>
          <p className="text-gray-400">Draft: {draft}</p>
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">Passing Stats</h2>
        <div className="grid grid-cols-2 gap-4 text-gray-300">
          <p>Yards: {stats.passing.passingYards}</p>
          <p>Touchdowns: {stats.passing.passingTouchdowns}</p>
          <p>Interceptions: {stats.passing.interceptions}</p>
          <p>Completion %: {stats.passing.completionPct.toFixed(1)}</p>
          <p>Yards/Attempt: {stats.passing.yardsPerPassAttempt}</p>
          <p>QB Rating: {stats.passing.QBRating}</p>
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">Rushing Stats</h2>
        <div className="grid grid-cols-2 gap-4 text-gray-300">
          <p>Yards: {stats.rushing.rushingYards}</p>
          <p>Touchdowns: {stats.rushing.rushingTouchdowns}</p>
          <p>Attempts: {stats.rushing.rushingAttempts}</p>
          <p>Yards/Attempt: {stats.rushing.yardsPerRushAttempt}</p>
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">Receiving Stats</h2>
        <div className="grid grid-cols-2 gap-4 text-gray-300">
          <p>Yards: {stats.receiving.receivingYards}</p>
          <p>Touchdowns: {stats.receiving.receivingTouchdowns}</p>
          <p>Receptions: {stats.receiving.receptions}</p>
          <p>Yards/Reception: {stats.receiving.yardsPerReception}</p>
        </div>
      </div>
    </div>
  );
}
