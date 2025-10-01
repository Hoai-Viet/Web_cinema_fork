import { Search, User, Ticket, Popcorn } from "lucide-react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between font-anton py-3 shadow-none border-b-1 border-white px-40 bg-[#000235]">
      {/* Logo */}
      <Link to={"/"} className="text-lg text-white">
        Logo
      </Link>

      {/* Button */}
      <div className="flex space-x-3">
        <button className="flex items-center gap-2 bg-[#433D8B] text-white hover:bg-[#6554AF] px-4 py-2 rounded-[10px] text-sm cursor-pointer">
          <Ticket className="w-5 h-5 text-white" />
          BUY TICKETS
        </button>
        <button className="flex items-center gap-2 bg-[#864AF9] text-white hover:bg-[#AA77FF] px-4 py-2 rounded-[10px] text-sm cursor-pointer">
          <Popcorn className="w-5 h-5 text-white" />
          BUY POPCORN
        </button>
      </div>

      <div className="flex items-center gap-4 pr-4">
        {/* Search box */}
        <div className="flex items-center border rounded-[10px] overflow-hidden w-64 bg-white">
          <input
            type="text"
            placeholder="Find movies, thearters"
            className="px-3 py-2 w-full outline-none text-sm"
          />
          <button className="px-3 text-gray-600 hover:text-black">
            <Search className="w-5 h-5 hover:cursor-pointer" />
          </button>
        </div>

        {/* Sign in */}
        <Link to={"/login"}>
          <button className="flex items-center gap-2 text-sm text-white hover:text-[#A555EC] cursor-pointer ">
            <User className="w-5 h-5" />
            Sign in
          </button>
        </Link>
      </div>
    </nav>
  );
}
