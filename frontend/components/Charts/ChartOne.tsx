"use client";

import { ApexOptions } from "apexcharts";
import React, { useState } from "react";
import ReactApexChart from "react-apexcharts";
import DefaultSelectOption from "@/components/SelectOption/DefaultSelectOption";

const ChartOne: React.FC = () => {
  const [isSwapped, setIsSwapped] = useState(false);

  const toggleSwap = () => {
    setIsSwapped(!isSwapped);
  };

  // Original Series
  const originalSeries = [
    {
      name: "Received Amount",
      data: [0, 20, 35, 45, 35, 55, 65, 50, 65, 75, 60, 75],
    },
    {
      name: "Due Amount",
      data: [15, 9, 17, 32, 25, 68, 80, 68, 84, 94, 74, 62],
    },
  ];

  // Swapped Series (Categories become data points)
  const swappedSeries = originalSeries.map((series) => ({
    ...series,
    data: series.data.map((value, index) => ({
      x: [
        "Sep",
        "Oct",
        "Nov",
        "Dec",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
      ][index],
      y: value,
    })),
  }));

  const series = isSwapped ? swappedSeries : originalSeries;

  const options: ApexOptions = {
    legend: {
      show: false,
      position: "top",
      horizontalAlign: "left",
    },
    colors: ["#5750F1", "#0ABEF9"],
    chart: {
      fontFamily: "Satoshi, sans-serif",
      height: 310,
      type: isSwapped ? "bar" : "area", // Switch chart type
      stacked: isSwapped, // Enable stacking for swapped bar chart
      toolbar: {
        show: false,
      },
    },
    fill: {
      gradient: {
        opacityFrom: 0.55,
        opacityTo: 0,
      },
    },
    responsive: [
      {
        breakpoint: 1024,
        options: {
          chart: {
            height: isSwapped ? 300 : 300,
            type: isSwapped ? "bar" : "area",
          },
        },
      },
      {
        breakpoint: 1366,
        options: {
          chart: {
            height: isSwapped ? 320 : 320,
            type: isSwapped ? "bar" : "area",
          },
        },
      },
    ],
    stroke: {
      curve: isSwapped ? undefined : "smooth",
    },
    markers: {
      size: 0,
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
    dataLabels: {
      enabled: false,
    },
    tooltip: {
      fixed: {
        enabled: false,
      },
      x: {
        show: true, // Show X tooltip when swapped
      },
      y: {
        title: {
          formatter: function () {
            return "";
          },
        },
      },
      marker: {
        show: false,
      },
    },
    xaxis: {
      type: isSwapped ? "category" : "category",
      categories: isSwapped
        ? originalSeries[0].data.map(
            (_, index) =>
              [
                "Sep",
                "Oct",
                "Nov",
                "Dec",
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
              ][index]
          )
        : [
            "Sep",
            "Oct",
            "Nov",
            "Dec",
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
          ],
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
      title: {
        text: isSwapped ? "Amount ($)" : "Month",
        style: {
          fontSize: "14px",
          fontWeight: "bold",
          color: "#333",
        },
      },
    },
    yaxis: {
      title: {
        text: isSwapped ? "Month" : "Amount ($)",
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
  };

  return (
    <div className="col-span-12 rounded-[10px] bg-white px-7.5 pb-6 pt-7.5 shadow-1 dark:bg-gray-dark dark:shadow-card xl:col-span-7">
      <div className="mb-3.5 flex flex-col gap-2.5 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h4 className="text-body-2xlg font-bold text-dark dark:text-white">
            Payments Overview
          </h4>
        </div>
        <div className="flex items-center gap-2.5">
          <p className="font-medium uppercase text-dark dark:text-dark-6">
            Sort by:
          </p>
          <DefaultSelectOption options={["Monthly", "Yearly"]} />
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
        <div className="-ml-4 -mr-5">
          <ReactApexChart
            options={options}
            series={series}
            type={isSwapped ? "bar" : "area"}
            height={310}
          />
        </div>
      </div>

      <div className="flex flex-col gap-2 text-center xsm:flex-row xsm:gap-0">
        <div className="border-stroke dark:border-dark-3 xsm:w-1/2 xsm:border-r">
          <p className="font-medium">Received Amount</p>
          <h4 className="mt-1 text-xl font-bold text-dark dark:text-white">
            $45,070.00
          </h4>
        </div>
        <div className="xsm:w-1/2">
          <p className="font-medium">Due Amount</p>
          <h4 className="mt-1 text-xl font-bold text-dark dark:text-white">
            $32,400.00
          </h4>
        </div>
      </div>
    </div>
  );
};

export default ChartOne;
