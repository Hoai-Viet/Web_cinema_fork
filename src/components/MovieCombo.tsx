import { useEffect, useState } from "react";

interface Combo {
  id: string;
  name: string;
  description: string;
  price: number;
  image_url: string;
  quantity?: number;
}

interface ComboProps {
  totalTicketQty: number;
  onChangeComboTotal: (total: number, list: Combo[]) => void;
  onLoaded: (
    comboList: { id: string; name: string; quantity: number }[]
  ) => void;
}

export default function MovieCombo({
  totalTicketQty,
  onChangeComboTotal,
  onLoaded,
}: ComboProps) {
  const [combos, setCombos] = useState<Combo[]>([]);
  const [quantities, setQuantities] = useState<Record<string, number>>({});

  useEffect(() => {
    fetch("https://web-cinema-be.onrender.com/combo")
      .then((res) => res.json())
      .then((data) => {
        setCombos(data);

        const init: Record<string, number> = {};
        data.forEach((c: Combo) => (init[c.id] = 0));
        setQuantities(init);
      });
  }, []);

  const changeQty = (id: string, diff: number) => {
    setQuantities((prev) => {
      const currentTotal = Object.values(prev).reduce((s, q) => s + q, 0);

      if (diff > 0 && currentTotal >= totalTicketQty) {
        return prev;
      }

      const newQty = Math.max(0, (prev[id] || 0) + diff);

      return {
        ...prev,
        [id]: newQty,
      };
    });
  };

  useEffect(() => {
    const list = combos
      .map((c) => ({
        ...c,
        quantity: quantities[c.id] || 0,
      }))
      .filter((c) => c.quantity! > 0);

    const total = list.reduce((sum, c) => sum + c.price * c.quantity!, 0);

    onChangeComboTotal(total, list);

    onLoaded(
      list.map((c) => ({
        id: c.id,
        name: c.name,
        quantity: c.quantity!,
      }))
    );
  }, [quantities, combos]);

  return (
    <div className="text-white mb-10">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 font-roboto-light">
        {combos.map((c) => (
          <div
            key={c.id}
            className="bg-[#1B1A3B] p-5 rounded-xl shadow-lg flex gap-4 items-start"
          >
            {/* IMAGE */}
            <img
              src={c.image_url}
              className="w-28 h-32 object-cover rounded-lg shadow-xl"
            />

            {/* TEXT */}
            <div className="flex-1">
              <p className="text-xl uppercase">{c.name}</p>

              <p className="text-sm text-gray-200 leading-relaxed mt-1">
                {c.description}
              </p>

              <p className="text-md text-yellow-300 mt-2">
                {c.price.toLocaleString()} USD
              </p>

              {/* BUTTONS */}
              <div className="flex items-center mt-3 px-3 py-1 rounded-lg gap-4 w-fit">
                <button
                  onClick={() => changeQty(c.id, -1)}
                  className="px-3 py-1 bg-gray-600 rounded text-lg"
                >
                  –
                </button>

                <span className="w-4 text-center">{quantities[c.id]}</span>

                <button
                  onClick={() => changeQty(c.id, +1)}
                  className="px-3 py-1 bg-gray-600 rounded text-lg"
                >
                  +
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
