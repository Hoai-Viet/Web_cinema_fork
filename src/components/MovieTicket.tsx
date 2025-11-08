import { useEffect, useState } from "react";

interface TicketType {
  id: string;
  name: string;
  description: string;
  base_price: number;
}

export default function MovieTickets({
  showtimeId,
}: {
  showtimeId: string | null;
}) {
  const [ticketTypes, setTicketTypes] = useState<TicketType[]>([]);
  const [quantities, setQuantities] = useState<Record<string, number>>({});

  useEffect(() => {
    if (!showtimeId) return;

    fetch(`http://127.0.0.1:5000/showtime/${showtimeId}/ticket-types`)
      .then((res) => res.json())
      .then((data) => {
        setTicketTypes(data);
        const init: Record<string, number> = {};
        data.forEach((t: TicketType) => (init[t.id] = 0));
        setQuantities(init);
      })
      .catch((err) => console.error("Error fetching ticket types:", err));
  }, [showtimeId]);

  const handleChange = (id: string, delta: number) => {
    setQuantities((prev) => ({
      ...prev,
      [id]: Math.max(0, (prev[id] || 0) + delta),
    }));
  };

  if (!showtimeId) return null;

  return (
    <div className="w-full max-w-6xl text-white font-anton mt-10">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {ticketTypes.map((t) => (
          <div
            key={t.id}
            className="border border-gray-400 rounded-lg p-6 bg-purple-900/80 hover:bg-purple-800 transition-all"
          >
            <h2 className="text-yellow-300 font-bold text-xl mb-1 uppercase">
              {t.name}
            </h2>
            <p className="text-yellow-400 uppercase text-sm">{t.description}</p>
            <p className="text-white text-lg mt-1">
              {t.base_price.toLocaleString()} VND
            </p>

            <div className="flex items-center gap-3 mt-4">
              <button
                onClick={() => handleChange(t.id, -1)}
                className="w-8 h-8 bg-gray-400 text-black rounded font-bold hover:bg-gray-300"
              >
                −
              </button>
              <span className="text-lg w-6 text-center">
                {quantities[t.id] || 0}
              </span>
              <button
                onClick={() => handleChange(t.id, 1)}
                className="w-8 h-8 bg-gray-400 text-black rounded font-bold hover:bg-gray-300"
              >
                +
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
