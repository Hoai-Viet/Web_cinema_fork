import { useEffect, useState } from "react";

interface UserProfile {
  id: string;
  username: string;
  email: string;
  birthday: string;
  password: string;
}

export default function ProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);

  const [editData, setEditData] = useState({
    username: "",
    email: "",
    birthday: "",
  });

  const [passwordData, setPasswordData] = useState({
    password: "",
    new_password: "",
    confirm_password: "",
  });

  const token = localStorage.getItem("token");

  // Load profile
  useEffect(() => {
    if (!token) return;

    fetch("https://web-cinema-be.onrender.com/user/me", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        setProfile(data);
        setEditData({
          username: data.username,
          email: data.email,
          birthday: data.birthday,
        });
      })
      .catch((err) => console.error(err));
  }, []);

  if (!profile) return <div className="text-white">Loading...</div>;

  // -------------------
  // Update Profile
  // -------------------
  const handleUpdateProfile = async () => {
    const res = await fetch("https://web-cinema-be.onrender.com/user/me", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(editData),
    });

    const data = await res.json();
    if (res.ok) {
      alert("Cập nhật thành công");
      setProfile({ ...profile, ...editData });
    } else {
      alert(data.error || "Lỗi cập nhật");
    }
  };

  // -------------------
  // Change Password
  // -------------------
  const handleChangePassword = async () => {
    if (passwordData.new_password !== passwordData.confirm_password) {
      alert("Mật khẩu xác nhận không khớp");
      return;
    }

    const res = await fetch(
      "https://web-cinema-be.onrender.com/user/me/change-password",
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          old_password: passwordData.password,
          new_password: passwordData.new_password,
        }),
      }
    );

    const data = await res.json();
    if (res.ok) {
      alert("Đổi mật khẩu thành công");
      setPasswordData({
        password: "",
        new_password: "",
        confirm_password: "",
      });
    } else {
      alert(data.error || "Lỗi đổi mật khẩu");
    }
  };

  return (
    <div className="min-h-screen bg-[#030334] text-white p-8 font-roboto-semibold">
      <div className="grid grid-cols-1 lg:grid-cols-[260px_1fr] gap-8">
        {/* LEFT SIDEBAR */}
        <div className="bg-white/10 p-6 rounded-xl flex flex-col items-center">
          <div className="w-40 h-40 bg-gray-300 rounded-full"></div>

          <p className="mt-4 text-lg text-center">{profile.username}</p>

          <button className="text-purple-400 mt-1 text-sm">
            Change Your Avatar
          </button>

          <button className="mt-6 text-purple-300">LOG OUT</button>
        </div>

        {/* RIGHT CONTENT */}
        <div className="flex flex-col gap-10">
          {/* CUSTOMER INFO */}
          <div>
            <h2 className="text-2xl mb-4">CUSTOMER INFORMATION</h2>

            <div className="bg-white p-6 rounded-xl text-black grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm mb-1">Username</label>
                <input
                  className="w-full border rounded-lg p-3"
                  value={editData.username}
                  onChange={(e) =>
                    setEditData({ ...editData, username: e.target.value })
                  }
                />
              </div>

              <div>
                <label className="block text-sm mb-1">Birthday</label>
                <input
                  type="date"
                  className="w-full border rounded-lg p-3"
                  value={editData.birthday}
                  onChange={(e) =>
                    setEditData({ ...editData, birthday: e.target.value })
                  }
                />
              </div>

              <div>
                <label className="block text-sm mb-1">Email</label>
                <input
                  className="w-full border rounded-lg p-3"
                  value={editData.email}
                  onChange={(e) =>
                    setEditData({ ...editData, email: e.target.value })
                  }
                />
              </div>

              <button
                className="mt-4 bg-yellow-400 px-6 py-2 rounded-lg text-black hover:bg-yellow-500"
                onClick={handleUpdateProfile}
              >
                SAVE CHANGES
              </button>
            </div>
          </div>

          {/* CHANGE PASSWORD */}
          <div>
            <h2 className="text-2xl mb-4">CHANGE PASSWORD</h2>

            <div className="bg-white p-6 rounded-xl text-black grid gap-5">
              <div>
                <label className="block text-sm mb-1">Old password</label>
                <input
                  type="password"
                  className="w-full border rounded-lg p-3"
                  value={passwordData.password}
                  onChange={(e) =>
                    setPasswordData({
                      ...passwordData,
                      password: e.target.value,
                    })
                  }
                />
              </div>

              <div>
                <label className="block text-sm mb-1">New password</label>
                <input
                  type="password"
                  className="w-full border rounded-lg p-3"
                  value={passwordData.new_password}
                  onChange={(e) =>
                    setPasswordData({
                      ...passwordData,
                      new_password: e.target.value,
                    })
                  }
                />
              </div>

              <div>
                <label className="block text-sm mb-1">
                  Confirm new password
                </label>
                <input
                  type="password"
                  className="w-full border rounded-lg p-3"
                  value={passwordData.confirm_password}
                  onChange={(e) =>
                    setPasswordData({
                      ...passwordData,
                      confirm_password: e.target.value,
                    })
                  }
                />
              </div>

              <button
                className="bg-gray-300 px-6 py-2 rounded-lg w-60 hover:bg-gray-400"
                onClick={handleChangePassword}
              >
                CHANGE PASSWORD
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
