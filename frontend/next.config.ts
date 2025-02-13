import type { NextConfig } from "next";

const nextConfig: NextConfig = {
	images: {
		remotePatterns: [
			{
				protocol: "https", // Allow only HTTPS
				hostname: "vanilla.futurecdn.net",
				pathname: "/**", // Allow all paths under this hostname
			},
			{
				protocol: "https",
				hostname: "cdn.mos.cms.futurecdn.net",
				pathname: "/**",
			},
			{
				protocol: "https",
				hostname: "s.yimg.com",
				pathname: "/**",
			},
			{
				protocol: "https",
				hostname: "i.kinja-img.com",
				pathname: "/**",
			},
			{
				protocol: "https",
				hostname: "img.youtube.com",
				pathname: "/**",
			},
			{
				protocol: "https",
				hostname: "www.engadget.com",
				pathname: "/**",
			},
			{
				protocol: "https",
				hostname: "www.polygon.com",
				pathname: "/**",
			},
		],
	},
};

export default nextConfig;
