export default function Profile() {
  return (
    <div className="text-white font-anton p-10 w-full max-w-3xl">
      <h1 className="text-4xl mb-6">My Profile</h1>

      <div className="bg-[#1a1a3b] p-6 rounded-[12px] space-y-4 text-lg">
        <p>Name: Demo User</p>
        <p>Email: demo@example.com</p>
        <p>Member since: 2024</p>

        {/* Sau này bạn fetch API user info rồi setstate là được */}
      </div>
    </div>
  );
}
