"use client";

import ArrowIcon from "@/app/assets/arrow-right.svg";
import cogImage from "@/app/assets/cog.png";
import cylinderImage from "@/app/assets/cylinder.png";
import noodleImage from "@/app/assets/noodle.png";
import Image from "next/image";
import {
  motion,
  useScroll,
  useTransform,
  useMotionValueEvent,
} from "framer-motion";
import { useRef } from "react";
import { useRouter } from "next/navigation";

export const Hero = () => {
  const router = useRouter();

  const handleClick = () => {
    router.push("/dashboard/uploadCsv");
  };
  const heroRef = useRef(null);
  const { scrollYProgress } = useScroll({
    target: heroRef,
    offset: ["start end", "end start"],
  });

  const translateY = useTransform(scrollYProgress, [0, 1], [150, -150]);

  useMotionValueEvent(translateY, "change", (latestValue) =>
    console.log(latestValue)
  );

  return (
    <section
      ref={heroRef}
      className="pt-8 pb-20 md:pt-5 md:pb-10 bg-[radial-gradient(ellipse_200vw_100vh_at_bottom_left,#183ec2,#eaeefe_100%)] overflow-x-clip"
    >
      <div className="container">
        <div className="md:flex items-center">
          <div className="md:w-[478px]">
            <h1 className="text-5xl md:text-7xl font-bold tracking-tigher bg-gradient-to-b from-black to-[#001e80] text-transparent bg-clip-text mt-6">
              Hyperlocal Excellence
            </h1>
            <p className="text-xl text-[#010d3e] tracking-tight mt-6">
              Transform your hyperlocal business with AI-powered inventory
              prediction that understands your local market better than ever
              before. Stay ahead of demand, not behind it.
            </p>
            <div className="flex gap-1 items-center mt-[30px]">
              <button onClick={handleClick} className="btn btn-primary">
                Get Started
              </button>
            </div>
          </div>

          <div className="mt-20 md:mt-0 md:h-[648px] md:flex-1 relative">
            <motion.img
              src={cogImage.src}
              alt="Cog image"
              className="md:absolute md:h-full md:w-auto md:max-w-none md:-left-6 lg:left-0"
              animate={{
                translateY: [-30, 30],
              }}
              transition={{
                repeat: Infinity,
                repeatType: "mirror",
                duration: 3,
                ease: "easeInOut",
              }}
            />
            <motion.img
              src={cylinderImage.src}
              alt="cylinder Image"
              width={220}
              height={220}
              className="hidden md:block -top-8 -left-32 md:absolute"
              style={{
                translateY: translateY,
              }}
            />
            <motion.img
              src={noodleImage.src}
              width={220}
              alt="noodleImage"
              className="hidden lg:block absolute top-[524px] left-[448px] rotate-[30deg]"
              style={{
                rotate: 30,
                translateY: translateY,
              }}
            />
          </div>
        </div>
      </div>
    </section>
  );
};
