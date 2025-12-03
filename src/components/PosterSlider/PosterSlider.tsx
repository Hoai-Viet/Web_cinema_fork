import { useEffect, useState } from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Navigate, useNavigate } from "react-router-dom";
import {
  faTags,
  faClock,
  faEarthAmericas,
} from "@fortawesome/free-solid-svg-icons";

interface Movie {
  id: number;
  title: string;
  poster_url: string;
  genre: string;
  country: string;
  duration_minutes: number;
}

export default function PosterSlider() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("https://web-cinema-be.onrender.com/movie/movies")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
        return res.json();
      })
      .then((data) => setMovies(data))
      .catch((err) => console.error("Error fetching movies:", err));
  }, []);

  const settings = {
    dots: false,
    infinite: false,
    speed: 250,
    slidesToShow: 4,
    slidesToScroll: 4,
    responsive: [
      {
        breakpoint: 1024,
        settings: { slidesToShow: 3, slidesToScroll: 3, infinite: true },
      },
      { breakpoint: 600, settings: { slidesToShow: 2, slidesToScroll: 2 } },
      { breakpoint: 480, settings: { slidesToShow: 1, slidesToScroll: 1 } },
    ],
  };

  return (
    <div className="max-w-[1200px] w-full h-[400px] gap-x-4">
      <Slider {...settings}>
        {movies.map((m) => (
          <div
            key={m.id}
            className="relative overflow-hidden"
            onClick={() => navigate(`/movie/${m.id}`)}
          >
            <img
              src={m.poster_url}
              alt={m.title}
              className="w-full h-[350px] object-cover border-white"
            />
            <div
              className="absolute inset-0 flex flex-col px-6 gap-y-1 justify-center items-start bg-black/65 opacity-0 h-[350px]
              hover:opacity-100 cursor-pointer transition-opacity duration-300"
            >
              <div className="text-white font-roboto-semibold mb-2 text-xl">
                <h1>{m.title}</h1>
              </div>
              <div className="flex items-center gap-1">
                <FontAwesomeIcon icon={faTags} className="text-yellow-300" />
                <p className="text-white">{m.genre}</p>
              </div>
              <div className="flex items-center gap-1">
                <FontAwesomeIcon
                  icon={faEarthAmericas}
                  className="text-yellow-300"
                />
                <p className="text-white">{m.country}</p>
              </div>
              <div className="flex items-center gap-1">
                <FontAwesomeIcon icon={faClock} className="text-yellow-300" />
                <p className="text-white">{m.duration_minutes} phút</p>
              </div>
            </div>
            <div className="flex justify-center items-center">
              <h2 className="text-white text-xl font-roboto-semibold mt-2">
                {m.title}
              </h2>
            </div>
          </div>
        ))}
      </Slider>
    </div>
  );
}
