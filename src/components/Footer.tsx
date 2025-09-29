import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFacebook,
  faYoutube,
  faSquareInstagram,
  faTwitter,
} from "@fortawesome/free-brands-svg-icons";

export default function Footer() {
  return (
    <footer className="flex items-center justify-between px-28 py-3 border-t-2 bg-[#FDFCF0]">
      {/* Logo */}
      <div className="fond-bold text-2xl">Logo</div>

      {/* About us */}
      <div className="flex items-center gap-8">
        <a
          href="https://www.linkedin.com/in/%C4%91%E1%BB%A9c-nguy%E1%BB%85n-an-253914356/"
          className="font-medium underline hover:text-yellow-600 cursor-pointer"
        >
          About us
        </a>
      </div>

      {/* Follow us */}
      <div className="flex flex-col gap-2">
        <div className="font-semibold underline"> Follow us</div>
        <ul className="flex items-center gap-5">
          <li>
            <a
              href="https://www.facebook.com/nguynduc611"
              className="hover:cursor-pointer"
            >
              <FontAwesomeIcon icon={faFacebook} />
            </a>
          </li>
          <li>
            <a
              href="https://www.youtube.com/watch?v=HgIhKsLI5Ag&list=RDHgIhKsLI5Ag&start_radio=1"
              className="hover:curosr-pointer"
            >
              <FontAwesomeIcon icon={faYoutube} />
            </a>
          </li>
          <li>
            <a href="https://x.com/CineStar" className="hover:cursor-pointer">
              <FontAwesomeIcon icon={faTwitter} />
            </a>
          </li>
          <li>
            <a
              href="https://www.instagram.com/duc_nguyen6114/"
              className="hover:cursor-pointer"
            >
              <FontAwesomeIcon icon={faSquareInstagram} />
            </a>
          </li>
        </ul>
      </div>
    </footer>
  );
}
