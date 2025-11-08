import { useState } from "react";
import MovieInFo from "../components/MovieInfo";
import MovieShowTime from "../components/MovieShowtimes";
import MovieTheater from "../components/MovieTheater";
import MovieTickets from "../components/MovieTicket";

export default function MovieDetail() {
  const [selectedShowtimeId, setSelectedShowtimeId] = useState<string | null>(
    null
  );

  return (
    <div className="flex flex-col justify-center items-center space-y-8">
      <MovieInFo />

      <h1 className="text-white font-anton text-3xl">SHOWTIMES</h1>
      {/* truyền callback để nhận showtime được chọn */}
      <MovieShowTime onSelectShowtime={setSelectedShowtimeId} />

      <h1 className="text-white font-anton text-3xl self-start">CINEMA LIST</h1>
      {/* truyền id để MovieTheater hiển thị đúng rạp */}
      <MovieTheater showtimeId={selectedShowtimeId} />
      <h1 className="text-white font-anton text-3xl">SELECT TICKETS</h1>
      <MovieTickets showtimeId={selectedShowtimeId} />
    </div>
  );
}
