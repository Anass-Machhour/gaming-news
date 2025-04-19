import Articles from "@/components/Articles";
import { JSX } from "react";

export default async function Home() {
	const text: string = "Gaming News";
	const length = text.length;
	const lst: string[] = [];

	for (let i = 0; i < length; i++) {
		lst.push(text[i]);
	}


	const fetchData = async (page: number) => {
		"use server";
		try {
			const apiUrl = `${process.env.NEXT_PUBLIC_API_WEBSITE}/api/news?page=${page}`;
			if (!apiUrl) {
				console.error("apiURL not found");
			}
			const response = await fetch(apiUrl, { cache: "no-cache" });

			if (!response.ok) throw new Error('Login failed')

			return response.json();
		} catch (error) {
			console.error(error);
		}
	};


	return (
		<main className="grid place-content-center min-h-[100dvh] w-full pb-32">
			<main className="flex flex-col min-h-screen w-screen px-3">
				<section className=" h-[70dvh]">
					<div className="relative size-full overflow-hidden bg-cover bg-fixed bg-center bg-no-repeat bg-custom-img">
						<div className="grid place-content-center min-h-full ">
							<div className="flex flex-row">
								{lst.map((elm, index): JSX.Element => {
									return (
										<p
											key={index}
											className="text-[10vw] cursor-pointer z-10 transition-all drop-shadow-2xl hover:scale-125 hover:font-medium hover:mx-1"
										>
											{elm === " " ? "\u00A0" : elm}
										</p>
									);
								})}
							</div>
							<div className="absolute size-full bg-gradient-to-t from-[#1E0922] via-[#1E0922]/50 z-0"></div>
						</div>
					</div>
				</section>
				<section className="w-full pt-[10dvh]">
					<Articles getData={fetchData} />
				</section>
			</main>
		</main>
	);
}
