import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true, // Required for GitHub Pages since we can't use Next.js Image Optimization
  },
  basePath: '/Hackathon-2-phases-2-3-4-5-', // GitHub Pages serves from subdirectory
  assetPrefix: '/Hackathon-2-phases-2-3-4-5-', // Assets also need to be served from subdirectory
};

export default nextConfig;
