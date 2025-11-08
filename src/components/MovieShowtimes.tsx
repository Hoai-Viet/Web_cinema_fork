import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

interface Showtime {
  id: string;
  movie_id: string;
  room: string;
  start_time: string;
  end_time: string;
}

interface MovieShowTimeProps {
  onSelectShowtime: (id: string) => void;
}

export default function MovieShowTime({
  onSelectShowtime,
}: MovieShowTimeProps) {
  const { id } = useParams<{ id: string }>();
  const [showtimes, setShowtimes] = useState<Showtime[]>([]);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [selectedShowtimeId, setSelectedShowtimeId] = useState<string | null>(
    null
  );

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/showtime/movies/${id}/showtimes`)
      .then((res) => res.json())
      .then((data) => setShowtimes(data))
      .catch((err) => console.error("Error fetching showtimes:", err));
  }, [id]);

  const groupedByDate = showtimes.reduce(
    (acc: Record<string, Showtime[]>, s) => {
      if (!s.start_time) return acc;
      const date = s.start_time.split(" ")[0];
      if (!acc[date]) acc[date] = [];
      acc[date].push(s);
      return acc;
    },
    {}
  );

  const dates = Object.keys(groupedByDate).sort();

  useEffect(() => {
    if (dates.length > 0 && !selectedDate) {
      setSelectedDate(dates[0]);
    }
  }, [dates, selectedDate]);

  const getDayOfWeek = (dateStr: string) => {
    const days = [
      "Sunday",
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
    ];
    const d = new Date(dateStr);
    return days[d.getDay()];
  };

  if (showtimes.length === 0)
    return (
      <p className="text-gray-400 text-center mt-4">
        There are currently no showtimes available for this movie.
      </p>
    );

  return (
    <div className="flex flex-col items-center text-white font-anton">
      {selectedDate && (
        <div className="w-full max-w-4xl space-y-4 text-white">
          {Object.keys(groupedByDate).map((date) => {
            const day = getDayOfWeek(date);
            const [yyyy, mm, dd] = date.split("-");
            return (
              <div key={date} className="flex items-center gap-4 justify-start">
                {/* Ô ngày */}
                <div className="flex flex-col items-center justify-center px-5 py-3 rounded-md bg-yellow-300 text-purple-800 w-28 h-[70px]">
                  <span>
                    {dd}/{mm}
                  </span>
                  <span>{day}</span>
                </div>

                {/* Các suất chiếu */}
                <div className="flex flex-wrap gap-4">
                  {groupedByDate[date].map((s) => {
                    const isSelected = selectedShowtimeId === s.id;
                    return (
                      <button
                        key={s.id}
                        onClick={() => {
                          setSelectedShowtimeId(s.id);
                          onSelectShowtime(s.id);
                        }}
                        className={`flex items-center justify-center px-6 py-3 border-2 rounded-md h-[70px] transition-all
                          ${
                            isSelected
                              ? "bg-yellow-300 text-purple-800 border-yellow-300"
                              : "border-yellow-300 text-yellow-300 hover:bg-yellow-300 hover:text-purple-800"
                          }`}
                      >
                        {s.start_time?.split(" ")[1].slice(0, 5)} {s.room}
                      </button>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
