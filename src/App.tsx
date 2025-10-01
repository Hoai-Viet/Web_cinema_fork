import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import AuthForm from "./components/AuthForm";
import Forgotpassword from "./components/Forgotpassword";
import Home from "./apps/home";

function App() {
  return (
    <div className="flex flex-col min-h-screen bg-[#000235]">
      <Navbar />
      <div className="flex flex-1 justify-center items-center w-full">
        {/* Nội dung giữ nổi phía trên */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<AuthForm />} />
          <Route path="/forgotpassword" element={<Forgotpassword />} />
        </Routes>
      </div>

      <Footer />
    </div>
  );
}

export default App;
