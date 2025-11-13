import { useEffect, useState } from "react";

interface Cinema {
  id: string;
  name: string;
  address: string;
  phone: string;
}

interface MovieTheaterProps {
  showtimeId: string | null;
  onSelectCinema: (cinemaId: string) => void; // callback lên MovieDetail
}

export default function MovieTheater({
  showtimeId,
  onSelectCinema,
}: MovieTheaterProps) {
  const [cinema, setCinema] = useState<Cinema | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedCinemaId, setSelectedCinemaId] = useState<string | null>(null);

  useEffect(() => {
    if (!showtimeId) return;

    setLoading(true);
    fetch(`http://127.0.0.1:5000/showtime/${showtimeId}/cinema`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch cinema info");
        return res.json();
      })
      .then((data) => setCinema(data))
      .catch((err) => console.error("Error fetching cinema:", err))
      .finally(() => setLoading(false));
  }, [showtimeId]);

  const handleSelectCinema = (id: string) => {
    setSelectedCinemaId(id);
    onSelectCinema(id); // gửi cinemaId ra ngoài
    console.log("✅ Rạp được chọn:", id);
  };

  if (!showtimeId) return null;

  return (
    <div className="w-full text-white font-anton">
      <h1 className="text-white font-anton text-3xl self-start">CINEMA LIST</h1>
      {cinema ? (
        <div
          className={`bg-[#4E56C0] rounded-lg p-6 shadow-md transform mt-4 ${
            loading ? "opacity-60 scale-[0.99]" : "opacity-100 scale-100"
          } flex justify-between items-center`}
        >
          {/* Thông tin rạp */}
          <div>
            <h2 className="text-yellow-300 text-2xl mb-2">{cinema.name}</h2>
            <p className="text-white text-lg">{cinema.address}</p>
            <p className="text-lg">{cinema.phone}</p>

            {loading && (
              <p className="text-gray-300 text-sm mt-2 italic">
                Đang tải thông tin rạp...
              </p>
            )}
          </div>

          {/* Nút chọn rạp */}
          <div>
            <button
              onClick={() => handleSelectCinema(cinema.id)}
              className={`px-5 py-2 rounded-md border-2 transition-all
                ${
                  selectedCinemaId === cinema.id
                    ? "bg-yellow-300 text-[#4E56C0] border-yellow-300"
                    : "border-yellow-300 text-yellow-300 hover:bg-yellow-300 hover:text-[#4E56C0]"
                }`}
            >
              {selectedCinemaId === cinema.id
                ? "✓ Chosen"
                : "Click here to choose"}
            </button>
          </div>
        </div>
      ) : (
        <p className="text-gray-400 mt-4">
          No cinema information found for this showtime.
        </p>
      )}
    </div>
  );
}
