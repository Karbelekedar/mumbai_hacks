"use client";

import avatar1 from "@/app/assets/avatar-1.png";
import avatar2 from "@/app/assets/avatar-2.png";
import avatar3 from "@/app/assets/avatar-3.png";
import avatar4 from "@/app/assets/avatar-4.png";
import avatar5 from "@/app/assets/avatar-5.png";
import avatar6 from "@/app/assets/avatar-6.png";
import avatar7 from "@/app/assets/avatar-7.png";
import avatar8 from "@/app/assets/avatar-8.png";
import avatar9 from "@/app/assets/avatar-9.png";
import Image from "next/image";
import { twMerge } from "tailwind-merge";
import { motion } from "framer-motion";
import React from "react";

const testimonials = [
  {
    text: "The demographic insights are incredible. We discovered our area has 65% working professionals, helping us optimize our dark store inventory for grab-and-go meals.",
    imageSrc: avatar1.src,
    name: "Rajesh Mehta",
    username: "@quickmart_delhi",
  },
  {
    text: "Our stockout incidents dropped by 75% within the first month. The AI predictions for our tech-hub locality are remarkably accurate.",
    imageSrc: avatar2.src,
    name: "Priya Sharma",
    username: "@priya_retail",
  },
  {
    text: "The system predicted increased demand for healthy snacks near our store due to a new fitness center. This hyper-local intelligence is game-changing.",
    imageSrc: avatar3.src,
    name: "Amit Patel",
    username: "@quickserve_mumbai",
  },
  {
    text: "We were perfectly stocked during an unexpected rainy season because the AI predicted a surge in comfort foods. Impressive local weather integration!",
    imageSrc: avatar4.src,
    name: "Deepak Kumar",
    username: "@inventory_pro",
  },
  {
    text: "Managing inventory across multiple dark stores in Bangalore was challenging until we found this solution. Now each micro-market is optimized perfectly.",
    imageSrc: avatar5.src,
    name: "Sarah Mathews",
    username: "@freshcart_pune",
  },
  {
    text: "The system's ability to predict festival-related demand spikes has reduced our waste by 40% while maintaining perfect stock levels.",
    imageSrc: avatar6.src,
    name: "Kavita Singh",
    username: "@smart_retail",
  },
  {
    text: "Real-time market intelligence helped us capitalize on local events we didn't even know about. Our revenue increased by 35% in just two months.",
    imageSrc: avatar7.src,
    name: "Ankit Verma",
    username: "@quickstore_guru",
  },
  {
    text: "The population intelligence feature helped us optimize our product mix perfectly for our university area dark store. Students love us!",
    imageSrc: avatar8.src,
    name: "Ravi Kumar",
    username: "@campusmart",
  },
  {
    text: "From local events to community patterns, this AI understands our market better than we did after 5 years of operation.",
    imageSrc: avatar9.src,
    name: "Neha Gupta",
    username: "@smartstore_blr",
  },
];

const firstColumn = testimonials.slice(0, 3);
const secondColumn = testimonials.slice(3, 6);
const thirdColumn = testimonials.slice(6, 9);

const TestimonialsColumn = (props: {
  className?: string;
  testimonials: typeof testimonials;
  duration?: number
}) => (
  <div className={props.className}>
    <motion.div
      animate={{ 
        translateY: "-50%"
      }}
      transition={{
        duration: props.duration || 10,
        repeat: Infinity,
        ease: "linear",
        repeatType: "loop",
      }}
      className="flex flex-col gap-6 pb-6"
    >
      {[...new Array(2)].fill(0).map((_, index) => (
        <React.Fragment key={index}>
          {props.testimonials.map(({ text, imageSrc, name, username }) => (
            <div className="card" key={text}>
              <div>{text}</div>
              <div className="flex items-center gap-2 mt-5">
                <Image
                  src={imageSrc}
                  alt={name}
                  width={40}
                  height={40}
                  className="h-10 w-10 rounded-full"
                />
                <div className="flex flex-col">
                  <div className="font-medium tracking-tight leading-5">
                    {name}
                  </div>
                  <div className="leading-5 tracking-tight">{username}</div>
                </div>
              </div>
            </div>
          ))}
        </React.Fragment>
      ))}
    </motion.div>
  </div>
);

export const Testimonials = () => {
  return (
    <section className="bg-white">
      <div className="container">
        <div className="section-heading">
          <div className="flex justify-center">
            <div className="tag">Success Stories</div>
          </div>
          <h2 className="section-title mt-5">What our partners say</h2>
          <p className="section-description">
            From neighborhood stores to urban dark stores, our AI-powered inventory prediction has become an essential tool for hyperlocal businesses across India.
          </p>
        </div>

        <div className="flex justify-center gap-6 mt-10 [mask-image:linear-gradient(to_bottom,transparent,black_25%,black_75%,transparent)] max-h-[738px] overflow-hidden">
          <TestimonialsColumn testimonials={firstColumn} duration={15} />
          <TestimonialsColumn
            testimonials={secondColumn}
            className="hidden md:block"
            duration={19}
          />
          <TestimonialsColumn
            testimonials={thirdColumn}
            className="hidden lg:block"
            duration={17}
          />
        </div>
      </div>
    </section>
  );
};