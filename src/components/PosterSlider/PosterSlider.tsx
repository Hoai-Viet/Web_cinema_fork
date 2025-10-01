import chi_nga_em_nang from "../../assets/poster/chi_nga_em_nang.jpg";

import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faTags,
  faClock,
  faEarthAmericas,
} from "@fortawesome/free-solid-svg-icons";

const posters = [
  {
    img: chi_nga_em_nang,
    name: "Chị Ngã Em Nâng",
    genre: "Horror",
    country: "Vietnam",
    duration: 100,
  },
  {
    img: chi_nga_em_nang,
    name: "A",
    genre: "Horror",
    country: "Vietnam",
    duration: 100,
  },
  {
    img: chi_nga_em_nang,
    name: "B",
    genre: "Horror",
    country: "Vietnam",
    duration: 100,
  },
  {
    img: chi_nga_em_nang,
    name: "C",
    genre: "Horror",
    country: "Vietnam",
    duration: 100,
  },
  {
    img: chi_nga_em_nang,
    name: "D",
    genre: "Horror",
    country: "Vietnam",
    duration: 100,
  },
];

export default function PosterSlider() {
  var settings = {
    dots: false,
    infinite: false,
    speed: 250,
    slidesToShow: 4,
    slidesToScroll: 4,
    initialSlide: 0,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 3,
          infinite: true,
          dots: false,
        },
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
          initialSlide: 2,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        },
      },
    ],
  };
  return (
    <div className="max-w-[1200px] w-full h-[400px] gap-x-4">
      <Slider {...settings}>
        {posters.map((d) => (
          <div className="relative overflow-hidden">
            <img src={d.img} alt="" className="w-full h-[350px] border-white" />
            <div
              className="absolute inset-0 flex flex-col px-6 gap-y-1 justify-center items-start bg-black/65 opacity-0 h-[350px] font-roboto-light
              hover:opacity-100 cursor-pointer transition-opacity duration-300"
            >
              {/* Name */}
              <div className="text-white font-roboto-semibold mb-2 text-xl">
                <h1>{d.name}</h1>
              </div>
              {/* Icon genre */}
              <div className="flex items-center gap-1">
                <FontAwesomeIcon icon={faTags} className="text-yellow-300" />
                <p className="text-white">{d.genre}</p>
              </div>

              {/* Icon country */}
              <div className="flex items-center gap-1">
                <FontAwesomeIcon
                  icon={faEarthAmericas}
                  className="text-yellow-300"
                />
                <p className="text-white">{d.country}</p>
              </div>

              {/* Icon duration */}
              <div className="flex items-center gap-1">
                <FontAwesomeIcon icon={faClock} className="text-yellow-300" />
                <p className="text-white">{d.duration}</p>
              </div>
            </div>
            <div className="flex justify-center items-center">
              <h2 className="text-white text-xl font-roboto-semibold mt-2">
                {d.name}
              </h2>
            </div>
          </div>
        ))}
      </Slider>
    </div>
  );
}
