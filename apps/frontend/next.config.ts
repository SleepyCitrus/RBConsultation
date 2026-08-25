import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",

  basePath: "/rift-staples",

  trailingSlash: true,

  // Mandatory for static platforms like GitHub Pages
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
