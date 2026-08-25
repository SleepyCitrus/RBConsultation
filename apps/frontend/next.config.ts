import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  // Mandatory for static platforms like GitHub Pages
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
  basePath: "/rift-staples",
};

export default nextConfig;
