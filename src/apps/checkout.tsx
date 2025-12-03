import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function formatShowtime(datetimeStr: string | null) {
  if (!datetimeStr) return "";

  const d = new Date(datetimeStr.replace(" ", "T"));

  const days = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];

  const dayName = days[d.getDay()];
  const h = d.getHours().toString().padStart(2, "0");
  const m = d.getMinutes().toString().padStart(2, "0");

  const dd = d.getDate().toString().padStart(2, "0");
  const mm = (d.getMonth() + 1).toString().padStart(2, "0");
  const yyyy = d.getFullYear();

  return `${h}:${m} ${dayName} ${dd}/${mm}/${yyyy}`;
}

export default function Checkout() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const { user, token } = useAuth();

  if (!state) return <div className="text-white p-10">No data available.</div>;

  const {
    selectedTickets = [],
    selectedCombos = [],
    selectedSeats = [],
    showtime_id,
    movieTitle,
    ageRating,
    theaterName,
    theaterAddress,
    startTime,
    room,
  } = state;

  /** PRICE CALCULATION **/
  const totalTickets = selectedTickets.reduce(
    (sum: number, t: any) => sum + t.base_price * t.quantity,
    0
  );

  const totalCombos = selectedCombos.reduce(
    (sum: number, c: any) => sum + c.price * c.quantity,
    0
  );

  const finalTotal = totalTickets + totalCombos;

  // ======================================================
  //              HANDLE PAYMENT + CREATE TICKETS
  // ======================================================
  const handlePayment = async () => {
    if (!user) {
      alert("You need to log in before making a payment.");
      navigate("/login");
      return;
    }

    try {
      // ============================
      // STEP 1 — CREATE PAYMENT
      // ============================
      const paymentPayload = {
        user_id: user.id,
        amount: finalTotal,
        payment_method: "Cash",
      };

      const resPay = await fetch("https://web-cinema-be.onrender.com/payment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(paymentPayload),
      });

      const payData = await resPay.json();

      if (!resPay.ok) {
        alert("Payment failed: " + JSON.stringify(payData));
        return;
      }

      const payment_id = payData.payment.id;

      // ============================
      // STEP 2 — PREPARE TICKET LIST
      // ============================
      const ticketsPayload = {
        payment_id: payment_id,
        user_id: user.id,
        showtime_id: showtime_id,

        tickets: selectedSeats.map((seat: any, index: number) => ({
          seat_id: seat.seat_id,
          ticket_type_id: selectedTickets[index]?.id,
          snack_id: selectedCombos[index]?.id || null,
        })),
      };

      // ============================
      // STEP 3 — CREATE TICKETS
      // ============================
      const resTicket = await fetch(
        "https://web-cinema-be.onrender.com/ticket",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(ticketsPayload),
        }
      );

      const ticketData = await resTicket.json();

      if (!resTicket.ok) {
        alert("Create ticket failed: " + JSON.stringify(ticketData));
        return;
      }

      alert("Payment successful! Tickets created.");

      navigate("/", {
        state: {
          payment: payData.payment,
          tickets: ticketData.ticket_ids,
          total: finalTotal,
          movieTitle,
          startTime,
        },
      });
    } catch (err) {
      console.error(err);
      alert("System error while processing payment & ticket.");
    }
  };

  // ======================================================
  //                         UI
  // ======================================================
  return (
    <div className="w-full min-h-screen bg-gradient-to-b from-[#030A28] to-[#0A0A2A] text-white px-12 py-12 font-roboto-semibold">
      <div className="bg-[#50589C] p-10 rounded-xl w-full max-w-3xl mx-auto shadow-lg border border-[#3B82F6]">
        {/* MOVIE + AGE */}
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-3xl text-yellow-300 tracking-wide">
              {movieTitle}
            </h2>
            <p className="text-yellow-300 text-lg mt-1">{ageRating}</p>
          </div>
        </div>

        {/* THEATER */}
        <div className="mt-4 text-[19px] leading-relaxed">
          <h2 className="text-white">{theaterName}</h2>
          <p className="text-white">{theaterAddress}</p>
        </div>

        {/* SHOWTIME */}
        <div className="mt-4 text-[19px] text-white">
          <p className="text-yellow-300">Showtime</p>
          <p className="mt-1">{formatShowtime(startTime)}</p>
        </div>

        {/* ROOM - TICKETS - TYPES */}
        <div className="mt-4 grid grid-cols-3 gap-y-3 text-white text-[19px]">
          <div>
            <p className="text-yellow-300">Room</p>
            <p>{room}</p>
          </div>

          <div>
            <p className="text-yellow-300">Tickets</p>
            <p>
              {selectedTickets.reduce((s: number, t: any) => s + t.quantity, 0)}
            </p>
          </div>

          <div>
            <p className="text-yellow-300">Ticket Type</p>
            <p>{selectedTickets.map((t: any) => t.name).join(", ")}</p>
          </div>
        </div>

        {/* GROUP SEATS */}
        <div className="w-full flex gap-20 mt-8 text-white text-[19px]">
          {Object.entries(
            selectedSeats.reduce((g: any, seat: any) => {
              if (!g[seat.seat_type]) g[seat.seat_type] = [];
              g[seat.seat_type].push(seat.seat_number);
              return g;
            }, {})
          ).map(([type, seats]: any) => (
            <div key={type} className="flex items-start gap-10">
              <div>
                <p className="text-yellow-300">Seat Type</p>
                <p className="font-bold">{type}</p>
              </div>
              <div>
                <p className="text-yellow-300">Seat Numbers</p>
                <p className="font-bold">{seats.join(", ")}</p>
              </div>
            </div>
          ))}
        </div>

        {/* SNACKS */}
        <div className="mt-8 text-[19px] text-white">
          <p className="text-yellow-300">Snacks</p>
          <p className="mt-1">
            {selectedCombos.length > 0
              ? selectedCombos
                  .map((c: any) => `${c.name} × ${c.quantity}`)
                  .join(", ")
              : "—"}
          </p>
        </div>

        {/* TOTAL */}
        <div className="border-t border-dotted border-white mt-8 pt-6 flex justify-between items-center text-3xl text-yellow-300">
          <span>TOTAL AMOUNT</span>
          <span className="text-white">{finalTotal.toLocaleString()} USD</span>
        </div>
      </div>

      {/* BUTTONS */}
      <div className="flex gap-6 justify-center mt-10">
        <button
          onClick={() => navigate(-1)}
          className="bg-[#FFE507] text-black px-10 py-3 rounded-lg hover:bg-yellow-400 transition"
        >
          GO BACK
        </button>

        <button
          onClick={handlePayment}
          className="bg-gray-500 text-gray-300 px-10 py-3 rounded-lg hover:cursor-pointer"
        >
          PAY NOW
        </button>
      </div>
    </div>
  );
}
