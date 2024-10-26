"use client";

import React, { useState } from "react";
import { ArrowUp, ArrowDown, Clock, TrendingUp, Building } from "lucide-react";
import {
  Card as ShadcnCard,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/components/ui/card";
import dynamic from "next/dynamic";

// Dynamically import ApexCharts
const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

const Card = ({ children, className = "" }) => (
  <div className={`bg-white rounded-lg shadow-md p-4 ${className}`}>
    {children}
  </div>
);

const transformDemandData = (storeData) => {
  if (!storeData?.short_term_predictions?.demand_changes)
    return { categories: [], series: [] };

  // Generate series for each category, starting at 0 and going to predicted_change (positive or negative)
  const series = storeData.short_term_predictions.demand_changes.map((change) => ({
    name: change.category,
    data: [0, parseFloat(change.predicted_change)], // Start at 0, go to actual change, positive or negative
  }));

  // Use "Start" and "Change" to show progression on the x-axis
  const categories = ["Start", "Change"];

  return { categories, series };
};

export default function DemandForecastingPage() {
  const [selectedStore, setSelectedStore] = useState("1");
  const [activeTab, setActiveTab] = useState("short");

  // Sample data (imported from your JSON)
  const data = {
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
          {
            category: "wellness products",
            predicted_change: "+10",
            confidence: "80",
            driving_factors: [
              "health and wellness focus",
              "emerging health-conscious consumers",
            ],
          },
          {
            category: "convenience meals",
            predicted_change: "+12",
            confidence: "90",
            driving_factors: ["work-from-home lifestyle", "high income level"],
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
    },
    "2": {
      short_term_predictions: {
        demand_changes: [
          {
            category: "health foods",
            predicted_change: "+10",
            confidence: "85",
            driving_factors: [
              "increasing health consciousness",
              "affluent family lifestyle",
            ],
          },
          {
            category: "wellness products",
            predicted_change: "+12",
            confidence: "80",
            driving_factors: ["luxury service demand", "health consciousness"],
          },
          {
            category: "eco-friendly products",
            predicted_change: "+8",
            confidence: "75",
            driving_factors: [
              "sustainable living focus",
              "environmentally conscious residents",
            ],
          },
        ],
        peak_hours: {
          changes: ["10 AM - 12 PM", "4 PM - 6 PM"],
          factors: ["affluent families shopping patterns", "retiree free time"],
        },
      },
    },
    "3": {
      short_term_predictions: {
        demand_changes: [
          {
            category: "snacks",
            predicted_change: "+5",
            confidence: "80",
            driving_factors: ["student segment", "convenience premium"],
          },
          {
            category: "instant foods",
            predicted_change: "+3",
            confidence: "75",
            driving_factors: ["student segment", "price sensitivity"],
          },
          {
            category: "beverages",
            predicted_change: "+4",
            confidence: "70",
            driving_factors: ["student segment", "convenience premium"],
          },
        ],
        peak_hours: {
          changes: ["12:00 PM - 2:00 PM", "5:00 PM - 7:00 PM"],
          factors: ["student class schedules", "after work activities"],
        },
      },
    },
    "4": {
      short_term_predictions: {
        demand_changes: [
          {
            category: "organic groceries",
            predicted_change: "+15",
            confidence: "85",
            driving_factors: [
              "increased health awareness",
              "seasonal produce availability",
            ],
          },
          {
            category: "home office supplies",
            predicted_change: "+10",
            confidence: "80",
            driving_factors: [
              "continued remote work trends",
              "back-to-school season",
            ],
          },
        ],
        peak_hours: {
          changes: ["10 AM - 12 PM", "5 PM - 7 PM"],
          factors: ["work-from-home schedules", "evening grocery runs"],
        },
      },
    },
    "5": {
      short_term_predictions: {
        demand_changes: [
          {
            category: "organic groceries",
            predicted_change: "+10",
            confidence: "85",
            driving_factors: ["health awareness", "seasonal trends"],
          },
          {
            category: "electronics",
            predicted_change: "-5",
            confidence: "70",
            driving_factors: ["economic slowdown", "market saturation"],
          },
        ],
        peak_hours: {
          changes: ["12:00 PM - 2:00 PM", "6:00 PM - 8:00 PM"],
          factors: ["lunch breaks", "evening shopping"],
        },
      },
    },
    "6": {
      short_term_predictions: {
        demand_changes: [
          {
            category: "organic produce",
            predicted_change: "+12",
            confidence: "85",
            driving_factors: ["increased health awareness", "seasonal trends"],
          },
          {
            category: "frozen foods",
            predicted_change: "-5",
            confidence: "70",
            driving_factors: [
              "shift towards fresh products",
              "warming weather",
            ],
          },
        ],
        peak_hours: {
          changes: ["5 PM - 7 PM", "11 AM - 1 PM"],
          factors: ["after-work shopping", "lunch hour"],
        },
      },
    },
  };

  const currentStoreData = data[selectedStore] || {
    short_term_predictions: {
      demand_changes: [],
      peak_hours: { changes: [], factors: [] },
    },
  };

  const chartData = transformDemandData(currentStoreData);
  const chartOptions = {
    chart: {
      type: "line",
      height: 350,
      toolbar: { show: true },
    },
    stroke: {
      curve: "smooth",
      width: 2,
    },
    dataLabels: { enabled: false },
    xaxis: {
      categories: chartData.categories, // "Start" and "Change" to show slanting effect
      labels: { show: false }, // Hide x-axis labels if desired
    },
    yaxis: {
      title: { text: "Percentage Increase (%)" },
      min: 0,
    },
    tooltip: {
      y: {
        formatter: (val) => `${val}%`,
      },
    },
    colors: ["#3b82f6", "#10b981", "#f97316"],
  };


  const renderMetricCard = (title, value, icon) => (
    <Card>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <h3 className="text-xl font-bold">{value}</h3>
        </div>
        {icon}
      </div>
    </Card>
  );

  const renderPredictionCard = (predictions) => (
    <Card>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-gray-900">Category Changes</h3>
        <TrendingUp className="h-4 w-4 text-blue-600" />
      </div>
      <div className="space-y-2">
        {predictions.map((pred, index) => (
          <div key={index} className="flex items-center justify-between">
            <span className="text-sm text-gray-500">{pred.category}</span>
            <div className="flex items-center space-x-2">
              <span className="text-xs text-gray-500">
                {pred.confidence}% confidence
              </span>
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
          </div>
        ))}
      </div>
    </Card>
  );

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

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {renderMetricCard(
          "Peak Hours",
          currentStoreData.short_term_predictions.peak_hours.changes[0],
          <Clock className="h-8 w-8 text-blue-600" />
        )}
        {renderMetricCard(
          "Top Growth Category",
          currentStoreData.short_term_predictions.demand_changes[0]?.category,
          <TrendingUp className="h-8 w-8 text-green-600" />
        )}
        {renderMetricCard(
          "Infrastructure Projects",
          currentStoreData.long_term_predictions?.infrastructure_development
            ?.projects?.length || 0,
          <Building className="h-8 w-8 text-purple-600" />
        )}
      </div>

      <Card className="mt-8 pr-4">
        <h3 className="text-lg font-semibold mb-4">
          Demand Changes Across Categories
        </h3>
        <Chart
          options={chartOptions}
          series={chartData.series}
          type="line" // Set type to line
          height={350}
        />
      </Card>

      <div className="mt-8">
        <div className="flex space-x-2 mb-4 border-b">
          {["short", "mid", "long"].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 text-sm font-bold text-white ${
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
                currentStoreData.short_term_predictions.demand_changes
              )}
              <Card>
                <h3 className="text-sm font-medium text-gray-900 mb-4">
                  Driving Factors
                </h3>
                <ul className="space-y-2">
                  {currentStoreData.short_term_predictions.peak_hours.factors.map(
                    (factor, index) => (
                      <li key={index} className="text-sm text-gray-600">
                        • {factor}
                      </li>
                    )
                  )}
                </ul>
              </Card>
            </div>
          )}
          {activeTab === "mid" && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card>
                <h3 className="text-sm font-medium text-gray-900 mb-4">
                  Emerging Categories
                </h3>
                {currentStoreData.mid_term_predictions?.emerging_categories.map(
                  (category, index) => (
                    <div key={index} className="mb-4">
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-medium">
                          {category.category}
                        </span>
                        <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                          {category.growth_potential}
                        </span>
                      </div>
                    </div>
                  )
                )}
              </Card>
              <Card>
                <h3 className="text-sm font-medium text-gray-900 mb-4">
                  Demographic Shifts
                </h3>
                {currentStoreData.mid_term_predictions?.demographic_shifts.map(
                  (shift, index) => (
                    <div key={index} className="mb-4">
                      <div className="text-sm font-medium">{shift.trend}</div>
                      <div className="text-xs text-gray-500 mt-1">
                        Impact: {shift.impact}
                      </div>
                    </div>
                  )
                )}
              </Card>
            </div>
          )}
          {activeTab === "long" && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card>
                <h3 className="text-sm font-medium text-gray-900 mb-4">
                  Population Evolution
                </h3>
                <ul className="space-y-2">
                  {currentStoreData.long_term_predictions?.population_evolution.changes.map(
                    (change, index) => (
                      <li key={index} className="text-sm text-gray-600">
                        • {change}
                      </li>
                    )
                  )}
                </ul>
              </Card>
              <Card>
                <h3 className="text-sm font-medium text-gray-900 mb-4">
                  Recommended Adaptations
                </h3>
                {currentStoreData.long_term_predictions?.recommended_adaptations.map(
                  (adaptation, index) => (
                    <div key={index} className="mb-4">
                      <div className="text-sm font-medium">
                        {adaptation.area}
                      </div>
                      <div className="text-xs text-gray-500 mt-1">
                        {adaptation.action} • {adaptation.timeline}
                      </div>
                      <div className="mt-1">
                        <span
                          className={`text-xs px-2 py-1 rounded ${
                            adaptation.priority === "high"
                              ? "bg-red-100 text-red-800"
                              : "bg-yellow-100 text-yellow-800"
                          }`}
                        >
                          {adaptation.priority} priority
                        </span>
                      </div>
                    </div>
                  )
                )}
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
