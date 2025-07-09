import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import React from 'react';

function App() {
  return (
    // This div will take up the full screen height (min-h-screen)
    // Have a dark background (bg-gray-900)
    // Center its content using flexbox (flex, items-center, justify-center)
    // Set text color to white (text-white)
    // Apply padding on all sides (p-8)
    <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center p-8">
      {/* This div acts as a card or container */}
      {/* It has a lighter background (bg-gray-800), rounded corners (rounded-lg) */}
      {/* Shadow (shadow-xl), and padding (p-6) */}
      <div className="bg-gray-800 p-6 rounded-lg shadow-xl text-center">
        {/* Main heading with large text (text-4xl), bold font (font-bold) */}
        {/* And a bottom margin (mb-4) */}
        <h1 className="text-4xl font-bold mb-4">
          Tailwind CSS is Working! 🎉
        </h1>

        {/* Paragraph with slightly smaller text (text-lg) and light gray color (text-gray-300) */}
        <p className="text-lg text-gray-300 mb-6">
          If you see this styled, your setup is correct.
        </p>

        {/* A button with a distinct background, hover effect, padding, and rounded corners */}
        <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-full transition duration-300 ease-in-out transform hover:scale-105">
          Get Started
        </button>
      </div>
    </div>
  );
}

export default App
