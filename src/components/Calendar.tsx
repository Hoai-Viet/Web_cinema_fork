import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCalendarDays } from "@fortawesome/free-solid-svg-icons";

export default function Calendar() {
  return (
    <div className="relative">
      <input
        type="date"
        min="1900-01-01"
        max="3000-12-31"
        className="w-full h-12 border rounded-[10px] px-3 py-2 hover:outline outline-auto duration-85 ease-in-out"
        placeholder="dd/mm/yyyy"
      />
      <div className="absolute inset-y-0 right-0 flex items-center px-3 pointer-events-none">
        <FontAwesomeIcon icon={faCalendarDays} className="w-5 h-5 " />
      </div>
    </div>
  );
}
