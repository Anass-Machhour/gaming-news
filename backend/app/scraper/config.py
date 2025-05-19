from dataclasses import dataclass
from typing import List


@dataclass
class Selector:
    tag: str
    class_: str


@dataclass
class WebsiteConfig:
    name: str
    url: str
    section_selector: Selector
    article_selector: Selector
    headline_selector: str
    thumbnail_selector: Selector


websites: List[WebsiteConfig] = [
    WebsiteConfig(
        name="Kotaku",
        url="https://kotaku.com/culture/news",
        section_selector=Selector("div", "sc-17uq8ex-0 fakHlO"),
        article_selector=Selector("div", "sc-cw4lnv-12 kQoJyO"),
        headline_selector="h1",
        thumbnail_selector=Selector("div", "sc-1eow4w5-3 hGpdBg"),
    ),
    WebsiteConfig(
        name="engadget",
        url="https://www.engadget.com/gaming/pc/",
        section_selector=Selector("div", "! mt-0 flex items-start justify-between"),
        article_selector=Selector("li", "mb-6 box-border"),
        headline_selector="h1",
        thumbnail_selector=Selector("div", "caas-img-container"),
    ),
    WebsiteConfig(
        name="pcgamer",
        url="https://www.pcgamer.com/games/",
        section_selector=Selector("div", "clear-both widget widget-dynamic widget-latest-top widget-dynamic-latest-top widget-dynamic-listv2 wdn-listv2-layout-sm-scroll wdn-listv2-layout-md-scroll flexi-carouzelize"),
        article_selector=Selector("li", "wdn-listv2-item item-slot- item-slot-color-"),
        headline_selector="h1",
        thumbnail_selector=Selector("div", "clear-both widget widget-contentparsed widget-content widget-contentparsed-content widget-content-parsed widget-content-parsed-content_document"),
    ),
    WebsiteConfig(
        name="polygon",
        url="https://www.polygon.com/pc",
        section_selector=Selector("div", "v7zk5q3"),
        article_selector=Selector("div", "duet--content-cards--content-card _15ic40z3 _15ic40z0 cmuha60"),
        headline_selector="h1",
        thumbnail_selector=Selector("div", "duet--layout--entry-body _4ljyn30"),
    ),  
]