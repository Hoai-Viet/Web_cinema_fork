import { useEffect, useState } from "react";

interface Combo {
  id: string;
  name: string;
  description: string;
  price: number;
  image_url: string;
}

export default function MovieCombo() {
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
    setQuantities((prev) => ({
      ...prev,
      [id]: Math.max(0, prev[id] + diff),
    }));
  };

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
