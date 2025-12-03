import { useState } from "react";
import MovieInfo from "../components/MovieInfo";
import MovieShowTime from "../components/MovieShowtimes";
import MovieTheater from "../components/MovieTheater";
import MovieSeat from "../components/MovieSeat";
import MovieTickets from "../components/MovieTicket";
import MovieCombo from "../components/MovieCombo";
import PaymentBar from "../components/Payment";
import { useNavigate } from "react-router-dom";

export default function MovieDetail() {
  const [selectedShowtimeId, setSelectedShowtimeId] = useState<string | null>(
    null
  );
  const [selectedCinemaId, setSelectedCinemaId] = useState<string | null>(null);
  const [selectedRoomId, setSelectedRoomId] = useState<string | null>(null);

  const [movieTitle, setMovieTitle] = useState<string | null>(null);
  const [ageRating, setAgeRating] = useState<string | null>(null);

  const [theaterName, setTheaterName] = useState<string | null>(null);
  const [theaterAddress, setTheaterAddress] = useState<string | null>(null);

  const [startTime, setStartTime] = useState<string | null>(null);
  const [room, setRoom] = useState<string | null>(null);

  const [selectedSeats, setSelectedSeats] = useState<
    { seat_id: string; seat_number: string; seat_type: string }[]
  >([]);

  const [selectedCombos, setSelectedCombos] = useState<any[]>([]);
  const [selectedTickets, setSelectedTickets] = useState<any[]>([]);

  const navigate = useNavigate();

  const totalTicketQty = selectedTickets.reduce(
    (sum: number, t: any) => sum + t.quantity,
    0
  );

  return (
    <div className="flex flex-col justify-center items-center space-y-8 ">
      {/* MOVIE INFO */}
      <MovieInfo
        onLoaded={(title, age) => {
          setMovieTitle(title);
          setAgeRating(age);
        }}
      />
      <h1 className="text-white font-anton text-3xl">SHOWTIMES</h1>
      {/* SHOWTIMES */}
      <MovieShowTime
        onSelectShowtime={(showtimeId, roomId) => {
          setSelectedShowtimeId(showtimeId);
          setSelectedRoomId(roomId);
        }}
        onLoaded={(startTime, room) => {
          setStartTime(startTime);
          setRoom(room);
        }}
      />

      {/* THEATER */}
      <MovieTheater
        showtimeId={selectedShowtimeId}
        selectedCinemaId={selectedCinemaId}
        onSelectCinema={(cinemaId) => setSelectedCinemaId(cinemaId)}
        onLoaded={(theaterName, theaterAddress) => {
          setTheaterName(theaterName);
          setTheaterAddress(theaterAddress);
        }}
      />

      {/* TICKET TYPES */}
      <MovieTickets
        showtimeId={selectedShowtimeId}
        onChangeTotal={(_, list) => setSelectedTickets(list)}
      />

      {/* SEATS */}
      {selectedCinemaId && (
        <MovieSeat
          showtimeId={selectedShowtimeId}
          roomId={selectedRoomId}
          onSelectSeats={(seatList) => setSelectedSeats(seatList)}
        />
      )}

      <h1 className="text-white font-anton text-3xl">COMBOS</h1>

      {/* COMBOS */}
      <MovieCombo
        totalTicketQty={totalTicketQty}
        onChangeComboTotal={(_, list) => setSelectedCombos(list)}
        onLoaded={() => {}}
      />

      {/* PAYMENT BAR */}
      {totalTicketQty > 0 &&
        selectedSeats.length === totalTicketQty &&
        selectedShowtimeId &&
        selectedCinemaId && (
          <PaymentBar
            selectedTickets={selectedTickets}
            selectedCombos={selectedCombos}
            onPay={() =>
              navigate("/checkout", {
                state: {
                  selectedTickets,
                  selectedCombos,
                  selectedSeats,

                  // ID QUAN TRỌNG — FIX 100%
                  showtime_id: selectedShowtimeId,
                  cinema_id: selectedCinemaId,
                  room_id: selectedRoomId,

                  // INFO MOVIE
                  movieTitle,
                  ageRating,

                  // CINEMA INFO
                  theaterName,
                  theaterAddress,

                  // TIME
                  startTime,
                  room,
                },
              })
            }
          />
        )}
    </div>
  );
}
