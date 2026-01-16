import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true, // Required for GitHub Pages since we can't use Next.js Image Optimization
  },
  basePath: '', // Will be updated based on your GitHub Pages path
  assetPrefix: '', // Will be updated based on your GitHub Pages path
};

export default nextConfig;
