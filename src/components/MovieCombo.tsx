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
    fetch("http://127.0.0.1:5000/combo")
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

      // Nếu bấm + nhưng tổng combo đã đủ số vé thì chặn lại
      if (diff > 0 && currentTotal >= totalTicketQty) {
        return prev; // KHÔNG tăng thêm
      }

      const newQty = Math.max(0, (prev[id] || 0) + diff);

      return {
        ...prev,
        [id]: newQty,
      };
    });
  };

  // Tính tổng + gửi ngược
  useEffect(() => {
    const list = combos
      .map((c) => ({
        ...c,
        quantity: quantities[c.id] || 0,
      }))
      .filter((c) => c.quantity! > 0);

    const total = list.reduce((sum, c) => sum + c.price * c.quantity!, 0);

    // Gửi luôn combo_id chuẩn
    onChangeComboTotal(total, list);

    // Gửi lên cả name + quantity + id
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
      <div className="grid grid-cols-1 md:grid-cols-3 gap-10 font-anton">
        {combos.map((c) => (
          <div key={c.id} className="flex flex-col items-center">
            <img
              src={c.image_url}
              className="w-40 h-40 object-cover rounded-lg shadow-lg"
            />

            <p className="mt-3 text-lg uppercase text-center">{c.name}</p>

            <p className="text-sm text-gray-300">
              {c.price.toLocaleString()} VND
            </p>

            <div className="flex items-center mt-3 bg-gray-700 px-3 rounded-lg gap-4">
              <button
                onClick={() => changeQty(c.id, -1)}
                className="px-3 py-1 bg-gray-600 rounded"
              >
                -
              </button>

              <span className="w-4 text-center">{quantities[c.id]}</span>

              <button
                onClick={() => changeQty(c.id, +1)}
                className="px-3 py-1 bg-gray-600 rounded"
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
