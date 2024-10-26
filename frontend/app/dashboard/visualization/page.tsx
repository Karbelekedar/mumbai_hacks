import ChartOne from "@/components/Charts/ChartOne";
import ChartThree from "@/components/Charts/ChartThree";
import ChartTwo from "@/components/Charts/ChartTwo";
import ProductCard from "@/components/Charts/ProductCard";
import React from "react";

const Visualization = () => {
  return (
    <div className="mt-4 grid grid-cols-12 gap-4 md:mt-6 md:gap-6 2xl:mt-9 2xl:gap-7.5">
      <ChartOne />
      <ProductCard />
      <ChartTwo />
      <ChartThree />
    </div>
  );
};

export default Visualization;
