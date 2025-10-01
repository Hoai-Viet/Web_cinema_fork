import ImageSlider from "./ImageSlider";
import chi_nga_em_nang from "../../assets/banner/chi_nga_em_nang_banner.jpg";
import rinh_qua from "../../assets/banner/rinh_qua.jpg";
import top_10_phim from "../../assets/banner/top_10_phim.jpg";

const IMAGES = [chi_nga_em_nang, rinh_qua, top_10_phim];

export default function ImageSliderContainer() {
  return (
    <div className="max-w-[1200px] w-full h-10/6 mx-auto mt-8">
      <ImageSlider imageUrls={IMAGES} />
    </div>
  );
}
