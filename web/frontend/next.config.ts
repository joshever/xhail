import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow the frontend to be deployed standalone on Vercel
  output: "standalone",
};

export default nextConfig;
