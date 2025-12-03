import { useEffect, useState } from "react";

interface Seat {
  id: string;
  seat_number: string;
  seat_type: string; // available | vip | booked
}

interface MovieSeatProps {
  showtimeId: string | null;
  roomId?: string | null;
  onSelectSeats?: (
    seats: { seat_id: string; seat_number: string; seat_type: string }[]
  ) => void;
}

export default function MovieSeat({
  showtimeId,
  onSelectSeats,
}: MovieSeatProps) {
  const [seats, setSeats] = useState<Seat[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!showtimeId) return;

    const fetchSeats = async () => {
      setLoading(true);
      try {
        const res = await fetch(
          `https://web-cinema-be.onrender.com/seat/${showtimeId}/seats`
        );
        if (!res.ok) throw new Error("Failed to load seats");
        const data = await res.json();
        setSeats(data);
      } catch (err) {
        console.error("Error fetching seats:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchSeats();
  }, [showtimeId]);

  const toggleSeat = (seat: Seat) => {
    if (seat.seat_type === "booked") return;

    setSelected((prev) =>
      prev.includes(seat.id)
        ? prev.filter((id) => id !== seat.id)
        : [...prev, seat.id]
    );
  };

  useEffect(() => {
    if (!onSelectSeats) return;

    const seatList = selected.map((id) => {
      const found = seats.find((s) => s.id === id);
      return {
        seat_id: found?.id || "",
        seat_number: found?.seat_number || "",
        seat_type: found?.seat_type || "",
      };
    });

    onSelectSeats(seatList);
  }, [selected, seats]);

  const grouped = seats.reduce((acc: Record<string, Seat[]>, s) => {
    const row = s.seat_number.charAt(0);
    if (!acc[row]) acc[row] = [];
    acc[row].push(s);
    return acc;
  }, {});

  const getSeatColor = (seat: Seat, isSelected: boolean) => {
    if (seat.seat_type === "booked")
      return "bg-red-600 opacity-60 cursor-not-allowed";
    if (isSelected) return "bg-yellow-500";
    if (seat.seat_type === "vip") return "bg-purple-600 hover:bg-purple-500";
    return "bg-gray-700 hover:bg-gray-600";
  };

  return (
    <div>
      {loading && <p className="text-white">Loading seats...</p>}

      {showtimeId && !loading && (
        <>
          <h1 className="text-white font-anton text-3xl text-center mb-4">
            SELECT SEATS
          </h1>

          <div className="flex flex-col gap-3 items-center mt-4">
            {Object.keys(grouped)
              .sort()
              .map((row) => (
                <div key={row} className="flex items-center gap-2">
                  <span className="text-white w-6">{row}</span>

                  {grouped[row]
                    .sort(
                      (a, b) =>
                        Number(a.seat_number.slice(1)) -
                        Number(b.seat_number.slice(1))
                    )
                    .map((seat) => {
                      const isSelected = selected.includes(seat.id);

                      return (
                        <button
                          key={seat.id}
                          onClick={() => toggleSeat(seat)}
                          disabled={seat.seat_type === "booked"}
                          className={`w-12 h-10 rounded-md text-xs text-white flex flex-col justify-center items-center ${getSeatColor(
                            seat,
                            isSelected
                          )}`}
                        >
                          <span>{seat.seat_number}</span>
                          <span className="text-[10px] opacity-80">
                            {seat.seat_type}
                          </span>
                        </button>
                      );
                    })}
                </div>
              ))}
          </div>
        </>
      )}
    </div>
  );
}
