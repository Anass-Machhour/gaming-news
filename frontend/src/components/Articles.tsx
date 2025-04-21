"use client";
import Image from "next/image";
import Link from "next/link";
import { useEffect, useState} from "react";

type ArticleType = {
	created_at: string; // ISO 8601 format date string
	headline: string;
	id: number;
	thumbnail_url: string;
	url: string;
	website_id: number;
};

type WebsiteType = {
	articles: ArticleType[];
	created_at: string; // ISO 8601 format date string
	favicon_url: string;
	id: number;
	name: string;
	url: string;
};

type DataType = {
	total_pages: number;
	results: WebsiteType[];
};

function Articles({ getData }: { getData: () => Promise<DataType> }) {
	const [isLoading, setIsLoading] = useState(true);
	const [articles, setArticles] = useState<ArticleType[]>([]);
	const [websites, setWebsites] = useState<WebsiteType[]>([]);

	useEffect(() => {
		const fetchData = async () => {
			try {
				const data: DataType = await getData();

				const websites: WebsiteType[] = data.results;

				const sortArticlesByDate = (data: WebsiteType[]) => {
					// Merge all the articles from all websites into a single list.
					const getArticles = data.flatMap((website) => website.articles);

					// Sort articles in descending order.
					return getArticles.sort(
						(a, b) =>
							new Date(b.created_at).getTime() -
							new Date(a.created_at).getTime()
					);
				};
				setArticles(sortArticlesByDate(websites));
				setWebsites(websites);
			} catch (error) {
				console.error(error);
			}
		};
		fetchData();
		setIsLoading(false);
	}, [getData]);

	if (isLoading || articles.length === 0) {
		return <p className="text-xl text-center">Loading...</p>;
	}

	return (
		<div className="flex gap-5 flex-wrap justify-center w-full">
			<div className="flex gap-5 flex-wrap justify-center w-full px-10">
				{articles.map((art, index) => {
					const website_id = art.website_id;
					const website = websites.find((item) => item.id === website_id);
					return (
						<article
							key={`article-${index}`}
							className="relative cursor-pointer w-[300px] sm:w-[350px]"
						>
							<Link href={art.url} target="_blank">
								<div className="absolute top-3 left-3 flex gap-1 items-center px-2 py-1 rounded-2xl bg-black/25 backdrop-blur-sm z-10">
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
								<div className="relative w-[300px] sm:w-[350px] h-40 sm:h-48 rounded-2xl ring-1 ring-blue-500 transition-all hover:ring-4 overflow-hidden">
									<Image
										src={art.thumbnail_url}
										alt={art.headline}
										title={art.headline}
										quality={75}
										fill
										priority
										className="object-cover"
									/>
								</div>
								<h2 title={art.headline} className="truncate py-4 text-sm">
									{art.headline}
								</h2>
							</Link>
						</article>
					);
				})}
			</div>
		</div>
	);
}

export default Articles;
