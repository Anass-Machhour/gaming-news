"use client"
export default function ErrorBoundary() {
	return (
		<div className="grid place-items-center w-full h-screen">
			<h1 className="text-[5vw] w-fit">Something come up :/</h1>
      <a href="/">Home page</a>
		</div>
	);
}