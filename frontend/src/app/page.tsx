import Articles from "@/components/Articles";
import { JSX } from "react";

export default function Home() {
	const text: string = "Gaming News";
	const length = text.length;
	const lst: string[] = [];

	for (let i = 0; i < length; i++) {
		lst.push(text[i]);
	}

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
					{/* <h3 className="text-5xl">Article</h3> */}
					{/* <div className="flex gap-5 flex-wrap justify-center w-full px-10">
						<article className="relative cursor-pointer max-w-[300px] sm:max-w-[350px]">
							<div className="absolute top-3 left-3 flex gap-2 items-center px-2 py-1 rounded-2xl bg-black/25 backdrop-blur-sm">
								<Image src={cozy} alt="" className="size-7 rounded-full" />
								<h3 className="truncate max-w-36 text-sm">name</h3>
							</div>
							<Image
								src={sea}
								alt=""
								title=""
								className="w-full h-auto rounded-2xl ring-1 transition-all hover:ring-4"
							/>
							<h2 className="truncate py-4 text-sm">
								Dolores beatae nam at sed dolorum ratione dolorem nisi velit
								cum.
							</h2>
						</article>
					</div> */}
					<Articles />
				</section>
			</main>
		</main>
	);
}
