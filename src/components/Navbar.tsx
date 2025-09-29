import { Search, User, Ticket, Popcorn } from "lucide-react";

export default function Navbar() {
  return (
    <nav
      className="flex items-center justify-between px-28 py-3 shadow-none border-b-2 "
      style={{ backgroundColor: "#FDFCF0" }}
    >
      {/* Logo */}
      <div className="font-bold text-lg">Logo</div>

      {/* Button */}
      <div className="flex space-x-3">
        <button className="flex items-center gap-2 border border-yellow-600 bg-[#FFEEB3] hover:bg-yellow-200 px-4 py-2 rounded-[10px] font-semibold text-sm cursor-pointer">
          <Ticket className="w-5 h-5" />
          BUY TICKETS
        </button>
        <button className="flex items-center gap-2 border border-yellow-600 bg-[#FFCB42] hover:bg-yellow-500 px-4 py-2 rounded-[10px] font-semibold text-sm cursor-pointer">
          <Popcorn className="w-5 h-5" />
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
        <button className="flex items-center gap-2 text-sm font-medium hover:text-yellow-600 cursor-pointer">
          <User className="w-5 h-5" />
          Sign in
        </button>
      </div>
    </nav>
  );
}
