import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowLeft, faArrowRight } from "@fortawesome/free-solid-svg-icons";

type ImageSliderProps = {
  imageUrls: string[];
};

export default function ImageSlider({ imageUrls }: ImageSliderProps) {
  const [imageIndex, setImageIndex] = useState(0);

  function showNextImage() {
    setImageIndex((index) => {
      if (index == imageUrls.length - 1) return 0;
      return index + 1;
    });
  }

  function showPrevImage() {
    setImageIndex((index) => {
      if (index == 0) return imageUrls.length - 1;
      return index - 1;
    });
  }

  return (
    <div className="relative w-full h-full">
      <div className="flex w-full h-full overflow-hidden">
        {imageUrls.map((url) => (
          <img
            key={url}
            src={url}
            className="block object-cover w-full h-full rounded-[4px] shrink-0 grow-0 duration-700 ease-in-out"
            style={{ transform: `translateX(${-100 * imageIndex}%)` }}
          />
        ))}
      </div>
      <button
        onClick={showPrevImage}
        className="absolute block top-1/2 text-white text-xl left-[-30px] 
                          hover:text-[#A555EC] cursor-pointer duration-75 ease-in-out"
      >
        <FontAwesomeIcon icon={faArrowLeft} />
      </button>
      <button
        onClick={showNextImage}
        className="absolute block top-1/2 text-white right-[-30px] text-xl 
                          hover:text-[#A555EC] cursor-pointer duration-75 ease-in-out"
      >
        <FontAwesomeIcon icon={faArrowRight} />
      </button>
    </div>
  );
}
