"use client";

import React, { useState } from "react";
import dynamic from "next/dynamic";
import { ArrowUp, ArrowDown, Clock, TrendingUp, Building } from "lucide-react";

// Dynamically import ApexCharts to avoid SSR issues
const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

// Types remain the same as before
interface DemandChange {
  category: string;
  predicted_change: string;
  confidence: string;
  driving_factors: string[];
}

interface PeakHours {
  changes: string[];
  factors: string[];
}

interface ShortTermPredictions {
  demand_changes: DemandChange[];
  peak_hours: PeakHours;
}

interface EmergingCategory {
  category: string;
  growth_potential: string;
  driving_factors: string[];
}

interface DemographicShift {
  trend: string;
  impact: string;
  category_implications: string[];
}

interface MidTermPredictions {
  emerging_categories: EmergingCategory[];
  demographic_shifts: DemographicShift[];
}

interface LongTermPredictions {
  population_evolution: {
    changes: string[];
    category_impacts: string[];
  };
  infrastructure_development: {
    projects: string[];
    business_implications: string[];
  };
  recommended_adaptations: {
    area: string;
    action: string;
    timeline: string;
    priority: string;
  }[];
}

interface StoreData {
  short_term_predictions: ShortTermPredictions;
  mid_term_predictions: MidTermPredictions;
  long_term_predictions: LongTermPredictions;
}

interface StoreDataMap {
  [key: string]: StoreData;
}

const transformDemandData = (stores: StoreDataMap) => {
  const categories: string[] = [];
  const changes: number[] = [];
  const confidence: number[] = [];

  Object.keys(stores).forEach((storeId) => {
    stores[storeId].short_term_predictions.demand_changes.forEach((change) => {
      categories.push(change.category);
      changes.push(parseFloat(change.predicted_change));
      confidence.push(parseFloat(change.confidence));
    });
  });

  return {
    categories,
    series: [
      { name: "Change", data: changes },
      { name: "Confidence", data: confidence },
    ],
  };
};

const Card = ({ children, className = "" }) => (
  <div className={`bg-white rounded-lg shadow-md p-4 ${className}`}>
    {children}
  </div>
);

export default function DemandForecastingPage() {
  const [selectedStore, setSelectedStore] = useState("1");
  const [activeTab, setActiveTab] = useState("short");

  // Sample data (same as before)
  const data: StoreDataMap = {
    "1": {
      short_term_predictions: {
        demand_changes: [
          {
            category: "home office",
            predicted_change: "+15",
            confidence: "85",
            driving_factors: [
              "increasing work-from-home population",
              "convenience premium",
            ],
          },
        ],
        peak_hours: {
          changes: ["12:00 PM - 2:00 PM", "6:00 PM - 8:00 PM"],
          factors: [
            "increased work-from-home flexibility",
            "demand for convenience meals",
          ],
        },
      },
      mid_term_predictions: {
        emerging_categories: [],
        demographic_shifts: [],
      },
      long_term_predictions: {
        population_evolution: {
          changes: [],
          category_impacts: [],
        },
        infrastructure_development: {
          projects: [],
          business_implications: [],
        },
        recommended_adaptations: [],
      },
    },
  };

  const getStoreData = (storeId: string): StoreData => {
    return (
      data[storeId] || {
        short_term_predictions: {
          demand_changes: [],
          peak_hours: { changes: [], factors: [] },
        },
        mid_term_predictions: {
          emerging_categories: [],
          demographic_shifts: [],
        },
        long_term_predictions: {
          population_evolution: { changes: [], category_impacts: [] },
          infrastructure_development: {
            projects: [],
            business_implications: [],
          },
          recommended_adaptations: [],
        },
      }
    );
  };

  const chartData = transformDemandData(data);
  const chartOptions = {
    chart: {
      type: "bar",
      height: 350,
      stacked: false,
      toolbar: {
        show: true,
      },
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "55%",
        endingShape: "rounded",
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      show: true,
      width: 2,
      colors: ["transparent"],
    },
    xaxis: {
      categories: chartData.categories,
    },
    yaxis: {
      title: {
        text: "Percentage (%)",
      },
    },
    fill: {
      opacity: 1,
    },
    tooltip: {
      y: {
        formatter: function (val: number) {
          return val + "%";
        },
      },
    },
    colors: ["#3b82f6", "#10b981"],
  };

  const renderPredictionCard = (
    title: string,
    predictions: DemandChange[],
    icon: React.ReactNode
  ) => {
    return (
      <Card>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-medium text-gray-900">{title}</h3>
          {icon}
        </div>
        <div className="space-y-2">
          {predictions.map((pred, index) => (
            <div key={index} className="flex items-center justify-between">
              <span className="text-sm text-gray-500">{pred.category}</span>
              <span
                className={`text-sm ${
                  pred.predicted_change.includes("+")
                    ? "text-green-600"
                    : "text-red-600"
                }`}
              >
                {pred.predicted_change}%
              </span>
            </div>
          ))}
        </div>
      </Card>
    );
  };

  return (
    <div className="p-4 space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Store Predictions Dashboard</h1>
        <div className="flex space-x-2">
          {[1, 2, 3, 4, 5, 6].map((store) => (
            <button
              key={store}
              onClick={() => setSelectedStore(store.toString())}
              className={`px-3 py-1 rounded transition-colors ${
                selectedStore === store.toString()
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 hover:bg-gray-300"
              }`}
            >
              Store {store}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Peak Hours</p>
              <h3 className="text-xl font-bold">
                {
                  getStoreData(selectedStore)?.short_term_predictions
                    ?.peak_hours?.changes?.[0]
                }
              </h3>
            </div>
            <Clock className="h-8 w-8 text-blue-600" />
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">
                Top Growth Category
              </p>
              <h3 className="text-xl font-bold">
                {
                  getStoreData(selectedStore)?.short_term_predictions
                    ?.demand_changes?.[0]?.category
                }
              </h3>
            </div>
            <TrendingUp className="h-8 w-8 text-green-600" />
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">
                Infrastructure Projects
              </p>
              <h3 className="text-xl font-bold">
                {getStoreData(selectedStore)?.long_term_predictions
                  ?.infrastructure_development?.projects?.length || 0}
              </h3>
            </div>
            <Building className="h-8 w-8 text-purple-600" />
          </div>
        </Card>
      </div>

      <Card className="mt-8">
        <h3 className="text-lg font-semibold mb-4">
          Demand Changes Across Categories
        </h3>
        <Chart
          options={chartOptions}
          series={chartData.series}
          type="bar"
          height={350}
        />
      </Card>

      <div className="mt-8">
        <div className="flex space-x-2 mb-4 border-b">
          {["short", "mid", "long"].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 text-sm font-medium ${
                activeTab === tab
                  ? "border-b-2 border-blue-600 text-blue-600"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)} Term
            </button>
          ))}
        </div>

        <div className="mt-4">
          {activeTab === "short" && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {renderPredictionCard(
                "Short Term Predictions",
                getStoreData(selectedStore)?.short_term_predictions
                  ?.demand_changes || [],
                <ArrowUp className="h-4 w-4 text-green-600" />
              )}
            </div>
          )}
          {activeTab === "mid" && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Mid-term predictions content */}
            </div>
          )}
          {activeTab === "long" && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Long-term predictions content */}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
