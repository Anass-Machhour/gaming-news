"use client";
import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

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

function Articles() {
	const [articles, setArticles] = useState<ArticleType[]>([]);
	const [isLoading, setIsLoading] = useState(true);
	const [totalPages, setTotalPages] = useState(1);
	const [websites, setWebsites] = useState<WebsiteType[]>([]);
	
	const router = useRouter();
	const pageParams = new URLSearchParams(useSearchParams());	
	const [page, setPage] = useState(1);

	const apiUrl = `${process.env.NEXT_PUBLIC_API_WEBSITE}/api/news?page=${page}`;

	useEffect(() => {

		const fetchData = async () => {
			try {
				if (!apiUrl) {
					console.error("apiURL not found");
				}

				const response = await fetch(apiUrl, { cache: "no-cache" });
				const data: DataType = await response.json();

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
				setTotalPages(data.total_pages);
				setWebsites(websites);
			} catch (error) {
				console.error(error);
			}
		};
		fetchData();
		router.push(`/news?${pageParams.toString()}`);
		setIsLoading(false);
	}, [page, apiUrl, pageParams, router]);

	const handlePrevious = () => {
		if (page > 1) {
			setPage(page - 1);
		}
		pageParams.set("page", page.toString());
		router.push(`/news?${pageParams.toString()}`);
		setIsLoading(true);
	};

	const handleNext = () => {
		if (page < totalPages) {
			setPage(page + 1);
		}
		pageParams.set("page", page.toString());
		router.push(`/news?${pageParams.toString()}`);
		setIsLoading(true);
	};

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
										sizes="400px"
										quality={100}
										fill
										priority
										className="bg-cover bg-center"
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
			<div className={`${isLoading ? "hidden" : "flex"} flex-row gap-5`}>
				<button disabled={page === 1} onClick={handlePrevious}>
					q
				</button>
				<p>
					{page}/{totalPages}
				</p>
				<button disabled={page === totalPages} onClick={handleNext}>
					p
				</button>
			</div>
		</div>
	);
}

export default Articles;
