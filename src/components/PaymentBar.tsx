import { useEffect, useState } from "react";

interface TicketType {
  id: string;
  name: string;
  base_price: number;
  quantity: number;
}

interface ComboType {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

export default function PaymentBar({
  selectedTickets,
  selectedCombos,
  onPay,
}: {
  selectedTickets: TicketType[];
  selectedCombos: ComboType[];
  onPay: () => void;
}) {
  const [total, setTotal] = useState(0);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(false);
    const timer = setTimeout(() => setMounted(true), 10);
    return () => clearTimeout(timer);
  }, [selectedTickets, selectedCombos]);

  useEffect(() => {
    const sum =
      selectedTickets.reduce((s, t) => s + t.base_price * t.quantity, 0) +
      selectedCombos.reduce((s, c) => s + c.price * c.quantity, 0);

    setTotal(sum);
  }, [selectedTickets, selectedCombos]);

  return (
    <div
      className={`
        w-full sticky bottom-0 bg-[#02061C] border-t border-[#FFE507] z-50 font-anton 
        transition-all duration-300 
        ${mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-5"}
      `}
    >
      <div className="w-full flex items-center justify-between px-10 py-4 text-white">
        <div className="flex flex-col">
          <p className="text-xl">Subtotal</p>
          <p className="text-3xl mt-1">{total.toLocaleString()} USD</p>
        </div>

        <button
          onClick={onPay}
          className="bg-[#FFE507] text-black px-10 py-4 rounded-lg text-lg cursor-pointer transition duration-150
           border-2 border-[#FFE507]
           hover:bg-black hover:text-[#FFE507]"
        >
          BUY TICKETS
        </button>
      </div>
    </div>
  );
}
