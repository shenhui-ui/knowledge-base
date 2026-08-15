---
type: ingest-note
source: marlin
date: 2026-08-03
---

# How I built a 500k-Domain Search Engine for Makers in a Weekend for $10

> Source: marlin

Sunday, 2am. I couldn’t sleep and I was annoyed at search engines again. Every query I actually cared about, portfolios, zines, weird little art projects, one-person software, drowned under a foot of corporate documentation and SEO sludge. So I did the thing you do at 2am: I opened a terminal and typed out a plan. “I want to make a search engine for myself only. There are 40-ish million domains. We can store a bit of metadata about each one. Even with 1KB each that’s 40GB, which is doable.” By Wednesday lunch I had 560,183 homepages catalogued, an empty queue of anything worth fetching next, and a decision to stop. This is the story of that weekend: what I built, what broke, what it cost, and what I’d tell you if you wanted to build your own. The headline, if you only read one paragraph: for about $10, an overnight GPU rental, and a few hours of steering the thing while it ran, you can have a personal search index of a few hundred thousand sites, under a gigabyte on disk. That’s the whole pitch. Everything below is how I got there and where the sharp edges are. Full technical details are provided separately .

## What I was actually trying to build

Not “index the web.” Just: find people doing stuff, art, code, hardware, poetry, little theatres, and not drown in docs.company.com . Personal, single user, no accounts. A crawler that only ever looks at homepages, a small local language model that reads each one and writes a name, two or three sentences, a category, and a handful of tags. A little search UI on top with fuzzy matching so I could type half a word and still find the right site. I wrote down what I was explicitly not building, mostly so that agents helping me wouldn’t quietly “simplify” it into something bigger: no IP scanning, no Redis, no storing full page HTML, no recrawl scheduler, nothing multi-tenant. Ignore was just a checkbox on a category, applied at search time. The crawler still summarised ecommerce sites, I just didn’t have to look at them. The napkin math was tens of millions of domains at roughly 1KB of metadata each, which is genuinely nothing for a Postgres box. Page text itself was never meant to be a corpus, just a scratch buffer that gets thrown away the moment the model is done with it.

## The machine

Four processes, three of them on my own PC, one rented GPU that never touches the database directly:

- A fetcher. Grabs a pending domain, tries HTTPS then HTTP, pulls the title, body text, and outbound links with a simple HTML parser, no JavaScript execution. Sets the row to “ready.”
- A worker. Grabs a ready domain, skips the model entirely if the page is empty, parked, or a bot-challenge wall, otherwise makes one structured request to a small local model (Gemma, 4B parameters) and gets back a name, summary, category, and tags. Wipes the scratch text, enqueues the outbound links at a priority based on what kind of page they came from.
- A steward. This one doesn’t touch the main queue at all. It samples domains from hosts that are producing suspiciously many pages, asks the model “block, keep, or unsure,” and quietly maintains a blocklist. More on why I needed this later.
- An API and a tiny web UI. Search with filters, a page to toggle which categories are hidden, and a dashboard so I could actually see what the factory was doing instead of squinting at logs.

Everything the fetcher grabs lives directly on the domain’s own database row while it’s “in progress.” Once the model is done with it, that text gets wiped. That matters more than it sounds, because at any real scale you cannot let raw page text pile up forever. Forty million rows times a few kilobytes each adds up fast, and I only needed that text for the few seconds the model was reading it.

## The web is 90% corporate, actually

The first version worked within a couple hours. Point it at a sample of domains, watch things get summarised, search for them. Great. Then, Sunday afternoon, I looked at what had actually been catalogued and it was the wrong web. Over 90% corporate sites and documentation. My seed list was skewed and the crawler had no opinions about what to chase next. The fix wasn’t to block anything. Blocking felt tempting but wrong, because a boring corporate docs page might still link out to someone’s personal blog, and I didn’t want to lose that. Instead I weighted the queue: pages classified as “portfolio” or “zine” or “software” push their outbound links way up the priority list, pages classified as “corporate” or “docs” push theirs down. One text file, `category-priority.txt` , became the steering wheel for the rest of the weekend. I’d tune a number, watch what came in over the next hour, tune again. That same afternoon I wiped the database twice because the quality was bad enough to just start over. Two bugs stood out: One site’s summary field just said “academic-profile,” a category label the model had shoved into the wrong slot. Fix: treat a susp