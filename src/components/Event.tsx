import discount3 from "../assets/event/discount3.png";
import discount2 from "../assets/event/discount2.png";
import discount4 from "../assets/event/discount4.png";
import discount5 from "../assets/event/discount5.png";

export default function Event() {
  return (
      <div className="flex justify-between gap-5 w-full mb-10">
        <img
          src={discount2}
          className="object-cover h-[200px] rounded-[10px] hover:cursor-pointer"
        />
        <img
          src={discount4}
          className="object-cover h-[200px] rounded-[10px] hover:cursor-pointer"
        />
        <img
          src={discount3}
          className="object-cover h-[200px] rounded-[10px] hover:cursor-pointer"
        />
        <img
          src={discount5}
          className="object-cover h-[200px] rounded-[10px] hover:cursor-pointer"
        />
      </div>
  );
}
