export default function Forgotpassword() {
  return (
    <div className="flex flex-col justify-between items-center w-128 h-98 border-3 p-8 my-12 border-[#D0A2F7] rounded-[10px] bg-white">
      <h1 className="font-semibold text-3xl text-[#A555EC]">FORGOT PASSWORD</h1>
      <p className="font-medium">
        Enter your email address and we'll send you instructions to create a new
        password
      </p>
      <input
        type="text"
        className="w-100 h-12 border border-black rounded-[10px] px-3 py-2 hover:outline outline-auto duration-85 ease-in-out"
        placeholder="Email"
      />
      <button className="w-100 h-12 rounded-[10px] bg-[#8F87F1] text-white hover:bg-[#A555EC] cursor-pointer">
        SEND VERIFICATION CODE
      </button>
    </div>
  );
}
