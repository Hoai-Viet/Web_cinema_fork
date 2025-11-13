import { useState } from "react";
import MovieInfo from "../components/MovieInfo";
import MovieShowTime from "../components/MovieShowtimes";
import MovieTheater from "../components/MovieTheater";
import MovieSeat from "../components/MovieSeat";
import MovieTickets from "../components/MovieTicket";
import MovieCombo from "../components/MovieCombo";

export default function MovieDetail() {
  const [selectedShowtimeId, setSelectedShowtimeId] = useState<string | null>(
    null
  );
  const [selectedCinemaId, setSelectedCinemaId] = useState<string | null>(null);
  const [selectedRoomId, setSelectedRoomId] = useState<string | null>(null);

  return (
    <div className="flex flex-col justify-center items-center space-y-8">
      <MovieInfo />

      <h1 className="text-white font-anton text-3xl">SHOWTIMES</h1>
      <MovieShowTime
        onSelectShowtime={(showtimeId, roomId) => {
          setSelectedShowtimeId(showtimeId);
          setSelectedRoomId(roomId);
        }}
      />

      <MovieTheater
        showtimeId={selectedShowtimeId}
        onSelectCinema={(cinemaId) => setSelectedCinemaId(cinemaId)}
      />      
      <MovieTickets showtimeId={selectedShowtimeId} />
      <MovieSeat showtimeId={selectedShowtimeId} roomId={selectedRoomId} />
      <h1 className="text-white font-anton text-3xl">COMBOS</h1>
      <MovieCombo />
    </div>
  );
}
