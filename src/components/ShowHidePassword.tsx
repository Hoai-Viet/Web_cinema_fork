import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

type ShowHidePasswordProps = {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder: string;
};

export default function ShowHidePassword({
  placeholder,
  value,
  onChange,
}: ShowHidePasswordProps) {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="relative">
      <input
        type={showPassword ? "text" : "password"}
        className="w-full h-12 border border-black rounded-[10px] px-3 py-2 hover:outline outline-auto duration-60 ease-in-out"
        placeholder={placeholder}
        onChange={onChange}
        value={value}
      />
      <button
        type="button"
        onClick={() => setShowPassword((prev) => !prev)}
        className="absolute inset-y-0 right-0 flex items-center px-3 cursor-pointer"
      >
        {showPassword ? (
          <FontAwesomeIcon icon={faEye} className="w-5 h-5" />
        ) : (
          <FontAwesomeIcon icon={faEyeSlash} className="w-5 h-5" />
        )}
      </button>
    </div>
  );
}
