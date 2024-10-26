"use client";

import { ApexOptions } from "apexcharts";
import React, { useState } from "react";
import ReactApexChart from "react-apexcharts";
import DefaultSelectOption from "@/components/SelectOption/DefaultSelectOption";

const ChartTwo: React.FC = () => {
  const [isSwapped, setIsSwapped] = useState(false);

  const toggleSwap = () => {
    setIsSwapped(!isSwapped);
  };

  // Original Series
  const originalSeries = [
    {
      name: "Sales",
      data: [44, 55, 41, 67, 22, 43, 65],
    },
    {
      name: "Revenue",
      data: [13, 23, 20, 8, 13, 27, 15],
    },
  ];

  // Swapped Series (Categories become data points)
  const swappedSeries = originalSeries.map((series) => ({
    ...series,
    data: series.data.map((value, index) => ({
      x: ["M", "T", "W", "T", "F", "S", "S"][index],
      y: value,
    })),
  }));

  const series = isSwapped ? swappedSeries : originalSeries;

  const options: ApexOptions = {
    colors: ["#5750F1", "#0ABEF9"],
    chart: {
      fontFamily: "Satoshi, sans-serif",
      type: "bar",
      height: isSwapped ? 335 : 335,
      stacked: isSwapped,
      toolbar: {
        show: false,
      },
      zoom: {
        enabled: false,
      },
      horizontal: isSwapped, // Switch to horizontal
    },
    responsive: [
      {
        breakpoint: 1536,
        options: {
          plotOptions: {
            bar: {
              borderRadius: 3,
              columnWidth: "25%",
              horizontal: isSwapped, // Maintain horizontal when responsive
            },
          },
        },
      },
    ],
    plotOptions: {
      bar: {
        horizontal: isSwapped, // Toggle horizontal
        borderRadius: 3,
        columnWidth: "25%",
        borderRadiusApplication: "end",
        borderRadiusWhenStacked: "last",
      },
    },
    dataLabels: {
      enabled: false,
    },
    grid: {
      strokeDashArray: 5,
      xaxis: {
        lines: {
          show: !isSwapped, // Hide X-axis lines when swapped
        },
      },
      yaxis: {
        lines: {
          show: isSwapped, // Show Y-axis lines when swapped
        },
      },
    },
    xaxis: {
      categories: isSwapped
        ? originalSeries[0].data.map(
            (_, index) => ["M", "T", "W", "T", "F", "S", "S"][index]
          )
        : ["M", "T", "W", "T", "F", "S", "S"],
      title: {
        text: isSwapped ? "Profit ($)" : "Day of the Week",
        style: {
          fontSize: "14px",
          fontWeight: "bold",
          color: "#333",
        },
      },
      labels: {
        rotate: isSwapped ? -45 : 0,
      },
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
    },
    yaxis: {
      title: {
        text: isSwapped ? "Day of the Week" : "Profit ($)",
        style: {
          fontSize: "14px",
          fontWeight: "bold",
          color: "#333",
        },
      },
      labels: {
        formatter: function (val) {
          return isSwapped ? val : val;
        },
      },
    },
    legend: {
      position: "top",
      horizontalAlign: "left",
      fontFamily: "Satoshi",
      fontWeight: 500,
      fontSize: "14px",
      markers: {
        radius: 99,
        width: 16,
        height: 16,
        strokeWidth: 10,
        strokeColor: "transparent",
      },
    },
    fill: {
      opacity: 1,
    },
  };

  return (
    <div className="col-span-12 rounded-[10px] bg-white px-10 pt-7.5 shadow-1 dark:bg-gray-dark dark:shadow-card xl:col-span-5">
      <div className="mb-4 justify-between gap-4 sm:flex">
        <div>
          <h4 className="text-body-2xlg font-bold text-dark dark:text-white">
            Profit this week
          </h4>
        </div>
        <div className="flex items-center gap-2.5">
          <DefaultSelectOption options={["This Week", "Last Week"]} />
          {/* Swap Axes Button */}
          <button
            onClick={toggleSwap}
            className="ml-4 rounded bg-blue-500 px-3 py-1 text-white hover:bg-blue-600"
          >
            Swap Axes
          </button>
        </div>
      </div>

      <div>
        <div id="chartTwo" className="-ml-3.5">
          <ReactApexChart
            options={options}
            series={series}
            type="bar"
            height={370}
          />
        </div>
      </div>
    </div>
  );
};

export default ChartTwo;
