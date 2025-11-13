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

    fetch(`http://127.0.0.1:5000/ticket/${showtimeId}/ticket-types`)
      .then((res) => res.json())
      .then((data) => {
        setTicketTypes(data);
        const init: Record<string, number> = {};
        if (Array.isArray(data)) {
          data.forEach((t: TicketType) => (init[t.id] = 0));
        }
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
    <div className="w-full max-w-6xl mx-auto text-white font-anton">
      <h1 className="text-white font-anton text-3xl text-center">SELECT TICKETS</h1>

      {ticketTypes.length === 0 ? (
        <p className="text-center text-gray-300 text-lg">
          No ticket types available for this showtime.
        </p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-4">
          {ticketTypes.map((t) => (
            <div key={t.id} className="border border-gray-500 rounded-xl p-6">
              <h2 className="text-yellow-300  text-xl">{t.name}</h2>
              <p className="text-white text-lg mt-2 font-normal">
                {t.base_price.toLocaleString()} VND
              </p>

              <div className="flex justify-center items-center gap-4 mt-5">
                <button
                  onClick={() => handleChange(t.id, -1)}
                  className="w-10 h-10 bg-gray-400 text-black rounded font-bold text-xl hover:bg-gray-300 transition"
                >
                  −
                </button>
                <span className="text-lg w-6 text-center select-none">
                  {quantities[t.id] || 0}
                </span>
                <button
                  onClick={() => handleChange(t.id, 1)}
                  className="w-10 h-10 bg-gray-400 text-black rounded text-xl hover:bg-gray-300 transition"
                >
                  +
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
