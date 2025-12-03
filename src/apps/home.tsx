import ImageSliderContainer from "../components/ImageSlider/ImageSliderContainer";
import PosterSlider from "../components/PosterSlider/PosterSlider";
import Event from "../components/Event";

export default function Home() {
  return (
    <div className="flex flex-col justify-center items-center space-y-8">
      <ImageSliderContainer />
      <h1 className="text-white font-anton text-4xl">NOW SHOWING</h1>
      <PosterSlider />
      <h1 className="text-white font-anton text-4xl mt-3">EVENT</h1>
      <Event />
    </div>
  );
}
