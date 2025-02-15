import Image from "next/image";
import Link from "next/link";

type Article = {
	created_at: string; // ISO date string
	headline: string;
	id: number;
	thumbnail_url: string;
	url: string;
	website_id: number;
};

type WebsiteData = {
	articles: Article[];
	created_at: string; // ISO date string
	favicon_url: string;
	id: number;
	name: string;
	url: string;
};

async function Articles() {
	try {
		const apiUrl = process.env.API_WEBSITE;

		if (!apiUrl) {
			throw new Error(
				"API_WEBSITE is not defined in the environment variables."
			);
		}
		const data: WebsiteData[] = await fetch(apiUrl, {
			cache: "force-cache",
		}).then((res) => res.json());

		return (
			<div className="flex gap-5 flex-wrap justify-center w-full px-10">
				{data.map((website) => {
					if (website["articles"].length === 0) {
						return;
					}
					return (
						<>
							{website.articles.map((art, index) => {
								return (
									<article
										key={index}
										className="relative cursor-pointer w-[300px] sm:w-[350px]"
									>
										<Link href={art.url} target="_blank">
											<div className="absolute top-3 left-3 flex gap-1 items-center px-2 py-1 rounded-2xl bg-black/25 backdrop-blur-sm">
												<Image
													src={website.favicon_url}
													alt={"${website.name}website Logo icon"}
													width={28}
													height={28}
													className="size-5 rounded-full border"
												/>
												<h3 className="truncate max-w-36 text-xs">
													{website["name"]}
												</h3>
											</div>
											<Image
												src={art.thumbnail_url}
												alt={art.headline}
												title={art.headline}
												width={400}
												height={400}
												className="w-[300px] sm:w-[350px] h-auto rounded-2xl ring-1 ring-blue-500 transition-all hover:ring-4"
											/>
											<h2 className="truncate py-4 text-sm">{art.headline}</h2>
										</Link>
									</article>
								);
							})}
						</>
					);
				})}
			</div>
		);
	} catch (error) {
		console.log(error)
		return (
			<h2 className="text-[3vw] text-center">Sorry no articles found :/</h2>
		);
	}
}

export default Articles;
