import { CallToAction } from "@/app/sections/CallToAction"
import { Footer } from "@/app/sections/Footer";
import { Header } from "@/app/sections/Header";
import { Hero } from "@/app/sections/Hero";
import { ProductShowcase } from "@/app/sections/ProductShowcase";
import { Testimonials } from "@/app/sections/Testimonials";
import { UploadCsv } from "@/app/dashboard/uploadCsv/page";

export default function Home() {
  return (
    <>
      {/* <Header />
      <Hero />
      <ProductShowcase />
      <Testimonials />
      <CallToAction /> */}
      {/* <Footer /> */}
      <UploadCsv />
    </>
  );
}
