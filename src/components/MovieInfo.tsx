import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faTags,
  faClock,
  faEarthAmericas,
  faClosedCaptioning,
  faUserCheck,
} from "@fortawesome/free-solid-svg-icons";

interface Movie {
  id: number;
  title: string;
  description: string;
  genre: string;
  country: string;
  duration_minutes: number;
  poster_url: string;
  age_rating?: string;
  language?: string;
}

export default function MovieInFo() {
  const { id } = useParams<{ id: string }>();
  const [movie, setMovie] = useState<Movie | null>(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/movie/movies/${id}`)
      .then((res) => res.json())
      .then((data) => setMovie(data))
      .catch((err) => console.error("Error fetching movie detail:", err));
  }, [id]);

  if (!movie)
    return <p className="text-white text-center mt-10">Đang tải...</p>;

  return (
    <div className="flex flex-col md:flex-row justify-center items-start text-white mt-10 gap-10">
      {/* Poster bên trái */}
      <div className="flex-shrink-0 w-full md:w-[350px]">
        <img
          src={movie.poster_url}
          alt={movie.title}
          className="rounded-lg shadow-lg w-full h-auto object-cover"
        />
      </div>

      {/* Thông tin phim bên phải */}
      <div className="flex flex-col gap-4 max-w-[700px]">
        {/* Tên phim + mã độ tuổi */}
        <div>
          <h1 className="text-4xl font-roboto-semibold uppercase">
            {movie.title}
          </h1>
        </div>

        {/* Thông tin chung */}
        <div className="flex flex-col gap-2 text-gray-300 mt-2">
          <div className="flex items-center gap-1">
            <FontAwesomeIcon icon={faTags} className="text-yellow-300" />
            <p className="text-white font-roboto-semibold">{movie.genre}</p>
          </div>
          <div className="flex items-center gap-1">
            <FontAwesomeIcon icon={faClock} className="text-yellow-300" />
            <p className="text-white font-roboto-semibold">
              {movie.duration_minutes}'
            </p>
          </div>
          <div className="flex items-center gap-1">
            <FontAwesomeIcon
              icon={faEarthAmericas}
              className="text-yellow-300"
            />
            <p className="text-white font-roboto-semibold">{movie.country}</p>
          </div>
          <div className="flex items-center gap-1">
            <FontAwesomeIcon
              icon={faClosedCaptioning}
              className="text-yellow-300"
            />
            <p className="text-white font-roboto-semibold">{movie.language}</p>
          </div>
          <div className="flex items-center gap-1">
            <FontAwesomeIcon icon={faUserCheck} className="text-yellow-300" />
            <p className="text-white font-roboto-semibold">
              {movie.age_rating}
            </p>
          </div>
        </div>

        {/* Nội dung phim */}
        {movie.description && (
          <div className="mt-6">
            <h2 className="text-xl font-roboto-semibold pb-2">
              MOVIE CONTENT
            </h2>
            <p className="text-gray-300 leading-relaxed">{movie.description}</p>
          </div>
        )}
      </div>
    </div>
  );
}
