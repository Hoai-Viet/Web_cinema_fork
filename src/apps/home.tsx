import ImageSliderContainer from "../components/ImageSlider/ImageSliderContainer";
import PosterSlider from "../components/PosterSlider/PosterSlider";
import Event from "../components/Event";
import MovieDetail from "./movie_detail";

export default function Home() {
  return (
    <div className="flex flex-col justify-center items-center space-y-8">
      <ImageSliderContainer />
      <h1 className="text-white font-anton text-4xl">NOW SHOWING</h1>
      <PosterSlider />
      <h1 className="text-white font-anton text-4xl">EVENT</h1>
      <Event />
    </div>
  );
}
