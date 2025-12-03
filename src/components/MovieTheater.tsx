import { useEffect, useState } from "react";

interface Cinema {
  id: string;
  name: string;
  address: string;
  phone: string;
}

interface MovieTheaterProps {
  showtimeId: string | null;
  selectedCinemaId: string | null;
  onSelectCinema: (cinemaId: string) => void;

  // sửa lại để trả cinema_id
  onLoaded: (name: string, address: string | null, cinemaId: string) => void;
}

export default function MovieTheater({
  showtimeId,
  selectedCinemaId,
  onSelectCinema,
  onLoaded,
}: MovieTheaterProps) {
  const [cinema, setCinema] = useState<Cinema | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!showtimeId) return;

    setLoading(true);
    fetch(`https://web-cinema-be.onrender.com/showtime/${showtimeId}/cinema`)
      .then((res) => res.json())
      .then((data) => {
        setCinema(data);

        // truyền luôn cinema.id
        onLoaded(data.name, data.address, data.id);
      })
      .catch((err) => console.error("Fetch cinema error:", err))
      .finally(() => setLoading(false));
  }, [showtimeId]);

  if (!showtimeId) return null;

  return (
    <div className="w-full text-white font-anton">
      <h1 className="text-white font-anton text-3xl self-start">CINEMA</h1>

      {cinema ? (
        <div
          className={`bg-[#4E56C0] rounded-lg p-6 shadow-md transform mt-4 
          ${loading ? "opacity-60 scale-[0.99]" : "opacity-100 scale-100"} 
          flex justify-between items-center`}
        >
          <div>
            <h2 className="text-yellow-300 text-2xl mb-2">{cinema.name}</h2>
            <p className="text-white text-lg">{cinema.address}</p>
            <p className="text-lg">{cinema.phone}</p>
          </div>

          <button
            onClick={() => onSelectCinema(cinema.id)}
            className={`px-5 py-2 rounded-md border-2 transition-all 
              ${
                selectedCinemaId === cinema.id
                  ? "bg-yellow-300 text-[#4E56C0] border-yellow-300"
                  : "border-yellow-300 text-yellow-300 hover:bg-yellow-300 hover:text-[#4E56C0]"
              }`}
          >
            {selectedCinemaId === cinema.id ? "✓ Chosen" : "Choose Cinema"}
          </button>
        </div>
      ) : (
        <p className="text-gray-400 mt-4">No cinema information.</p>
      )}
    </div>
  );
}
