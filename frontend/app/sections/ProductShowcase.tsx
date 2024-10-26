"use client";

import productImage from "@/app/assets/product-image.png";
import pyramidImage from "@/app/assets/pyramid.png";
import tubeImage from "@/app/assets/tube.png";
import Image from "next/image";
import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";

export const ProductShowcase = () => {
  const sectionRef = useRef(null);
  const { scrollYProgress } = useScroll({
    target: sectionRef,
    offset: ["start end", "end start"],
  });

  const translateY = useTransform(scrollYProgress, [0, 1], [150, -150]);

  return (
    <section
      ref={sectionRef}
      className="bg-gradient-to-b from-[#FFFFFF] to-[#D2DCFF] py-24 overflow-x-clip"
    >
      <div className="container">
        <div className="section-heading">
          <div className="flex justify-center items-center">
            <div className="tag">Boost your Inventory Intelligence</div>
          </div>
          <h2 className="section-title mt-5">
          A more effective way to predict demand
          </h2>
          <p className="section-description mt-5">
          Effortlessly transform your hyperlocal business with our advanced AI system that combines historical data, real-time market intelligence, and demographic insights to predict inventory needs with unprecedented accuracy.
          </p>
        </div>

        <div className="flex justify-center">
          <div className="relative max-w-[1000px]">
            <Image src={productImage} alt="product Image" className="mt-10 max-w-[800px]" />
            <motion.img
              src={pyramidImage.src}
              alt="pyramid Image"
              width={262}
              height={262}
              className="hidden md:block absolute -right-36 -top-32"
              style={{
                translateY
              }}
              />
          <motion.img
            src={tubeImage.src}
            alt="tube Image"
            width={248}
            height={248}
            className="hidden md:block absolute bottom-24 -left-36"
            style={{
              translateY
            }}
            />
        </div>
        </div>
      </div>
    </section>
  );
};
