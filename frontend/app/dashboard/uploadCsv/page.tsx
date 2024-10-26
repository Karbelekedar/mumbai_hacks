"use client";

import React, { useRef, useState } from "react";
import Papa from "papaparse";

interface CsvData {
  headers: string[];
  rows: string[][];
}

const UploadCsv: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [csvData, setCsvData] = useState<CsvData | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = () => {
    fileInputRef.current?.click();
  };

  const parseCSV = (file: File) => {
    const reader = new FileReader();
    reader.onload = (event) => {
      const csvText = event.target?.result as string;
      Papa.parse(csvText, {
        complete: (results) => {
          const headers = results.data[0] as string[];
          const rows = results.data.slice(1) as string[][];
          setCsvData({ headers, rows });
        },
        error: (error) => {
          console.error("Error parsing CSV:", error);
          alert("Error parsing CSV file");
        },
      });
    };
    reader.readAsText(file);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === "text/csv") {
      setSelectedFile(file);
      parseCSV(file);
      console.log("Selected file:", file.name);
    } else {
      alert("Please upload a CSV file.");
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);
    const file = event.dataTransfer.files[0];
    if (file && file.type === "text/csv") {
      setSelectedFile(file);
      parseCSV(file);
      console.log("Dropped file:", file.name);
    } else {
      alert("Please upload a CSV file.");
    }
  };

  const handleUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append("file", selectedFile);

      try {
        const response = await fetch("/api/upload", {
          method: "POST",
          body: formData,
        });
        if (response.ok) {
          alert("File uploaded successfully!");
          setSelectedFile(null);
          setCsvData(null);
        } else {
          alert("File upload failed.");
        }
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    }
  };

  return (
    <div className="flex flex-col">
      <h1 className="text-3xl font-semibold">Upload CSV</h1>

      {csvData ? (
        <div className="w-full">
          <div className="flex justify-between align-center mb-2 mt-4">
            <h2 className="text-xl font-semibold">{selectedFile?.name}</h2>
            <p className="text-gray-600 mb-4">
              Number of entries: {csvData.rows.length}
            </p>
          </div>
          <div className="mt-8 max-h-[500px] overflow-y-auto rounded-lg shadow-lg bg-white scrollbar-thin scrollbar-thumb-rounded-full">
            <table className="min-w-full bg-white rounded-lg overflow-hidden">
              <thead className="sticky top-0">
                <tr className="bg-blue-50">
                  {csvData.headers.map((header, index) => (
                    <th
                      key={index}
                      className="px-6 py-4 text-left text-sm font-semibold text-blue-900 border-b border-blue-100 first:rounded-tl-lg last:rounded-tr-lg"
                    >
                      {header}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-blue-100">
                {csvData.rows.map((row, rowIndex) => (
                  <tr
                    key={rowIndex}
                    className="hover:bg-blue-50 transition-colors duration-150 ease-in-out"
                  >
                    {row.map((cell, cellIndex) => (
                      <td
                        key={cellIndex}
                        className="px-6 py-4 text-sm text-gray-700 whitespace-nowrap"
                      >
                        {cell}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <button
            className="btn bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 mt-6 rounded-lg transition-colors duration-150 ease-in-out shadow-md"
            onClick={handleUpload}
          >
            Analyze
          </button>
        </div>
      ) : (
        <div
          className={`w-[80%] mt-4 py-72 ${
            isDragging ? "bg-blue-200" : "bg-blue-100"
          } flex justify-center items-center flex-col border-2 border-blue-300 border-dashed rounded-lg transition-colors duration-150 ease-in-out`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <button
            className="font-bold text-xl btn bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors duration-150 ease-in-out shadow-md"
            onClick={handleFileSelect}
          >
            Select CSV file
          </button>
          <p className="mt-4 text-blue-600">or drop CSV file here</p>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".csv"
            style={{ display: "none" }}
          />
        </div>
      )}
    </div>
  );
};

export default UploadCsv;
