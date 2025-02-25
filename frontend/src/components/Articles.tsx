import Image from "next/image";
import Link from "next/link";

type Article = {
	created_at: string; // ISO 8601 format date string
	headline: string;
	id: number;
	thumbnail_url: string;
	url: string;
	website_id: number;
};

type WebsiteData = {
	articles: Article[];
	created_at: string; // ISO 8601 format date string
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
			cache: "no-cache",
		}).then((res) => res.json());

		const articlesSortedByDate = (data: WebsiteData[]) => {
			// Merge all the articles from all websites into a single list.
			const getArticles = data.flatMap((website) => website.articles);

			// Sort articles in descending order.
			return getArticles.sort(
				(a, b) =>
					new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
			);
		};

		const articles = articlesSortedByDate(data);

		return (
			<div className="flex gap-5 flex-wrap justify-center w-full px-10">
				{articles.map((art, index) => {
					const website_id = art.website_id;
					const website = data.find((item) => item.id === website_id);
					return (
						<article
							key={`article-${index}`}
							className="relative cursor-pointer w-[300px] sm:w-[350px]"
						>
							<Link href={art.url} target="_blank">
								<div className="absolute top-3 left-3 flex gap-1 items-center px-2 py-1 rounded-2xl bg-black/25 backdrop-blur-sm">
									<Image
										src={website!.favicon_url}
										alt={`${website!.name}website Logo icon`}
										width={28}
										height={28}
										priority
										className="size-5 rounded-full border"
									/>
									<h3 className="truncate max-w-36 text-xs">{website!.name}</h3>
								</div>
								<Image
									src={art.thumbnail_url}
									alt={art.headline}
									title={art.headline}
									width={400}
									height={400}
									priority
									className="w-[300px] sm:w-[350px] h-40 sm:h-48 rounded-2xl ring-1 ring-blue-500 transition-all hover:ring-4"
								/>
								<h2 className="truncate py-4 text-sm">{art.headline}</h2>
							</Link>
						</article>
					);
				})}
			</div>
		);
	} catch (error) {
		console.log(error);
		return (
			<h2 className="text-[3vw] text-center">Sorry no articles found :/</h2>
		);
	}
}

export default Articles;
