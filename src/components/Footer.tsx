import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFacebook,
  faYoutube,
  faSquareInstagram,
  faTwitter,
} from "@fortawesome/free-brands-svg-icons";
import logo from "../assets/logo/logo.png";

export default function Footer() {
  return (
    <footer className="flex items-center justify-between font-anton py-5 border-t-1 border-white bg-[#000235] px-40">
      {/* Logo */}
      <img src={logo} alt="Logo" className="h-12" />

      {/* About us */}
      <div className="flex items-center gap-8">
        <a
          href="https://www.linkedin.com/in/%C4%91%E1%BB%A9c-nguy%E1%BB%85n-an-253914356/"
          className="text-white underline hover:text-[#A555EC] cursor-pointer"
        >
          About us
        </a>
      </div>

      {/* Follow us */}
      <div className="flex flex-col gap-2">
        <div className="underline text-white"> Follow us</div>
        <ul className="flex items-center gap-5">
          <li>
            <a
              href="https://www.facebook.com/nguynduc611"
              className="hover:cursor-pointer"
            >
              <FontAwesomeIcon icon={faFacebook} className="text-white" />
            </a>
          </li>
          <li>
            <a
              href="https://www.youtube.com/watch?v=HgIhKsLI5Ag&list=RDHgIhKsLI5Ag&start_radio=1"
              className="hover:curosr-pointer"
            >
              <FontAwesomeIcon icon={faYoutube} className="text-white" />
            </a>
          </li>
          <li>
            <a href="https://x.com/CineStar" className="hover:cursor-pointer">
              <FontAwesomeIcon icon={faTwitter} className="text-white" />
            </a>
          </li>
          <li>
            <a
              href="https://www.instagram.com/duc_nguyen6114/"
              className="hover:cursor-pointer"
            >
              <FontAwesomeIcon
                icon={faSquareInstagram}
                className="text-white"
              />
            </a>
          </li>
        </ul>
      </div>
    </footer>
  );
}
