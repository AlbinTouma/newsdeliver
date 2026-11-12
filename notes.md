## Features

User should be able to 

1) Point rss url and scrape its articles

```
newsdeliver --url https://bbc.com/rss > stream of articles
```

2) Point a list of rss urls and scrape them

```
newsdeliver --url https://bbc.com/rss, https://aftonbladet.com/rss > stream
```

3) Point an article url and get article

```
newsdeliver --article --url https://bbc.com/news/124
```

4) RSS Pipeline with workers

One RSS worker -> One URL fetcher -> One html parser


```
newsdeliver --pipeline --url https://bbc.com/rss, https://aftonbladet.com/rss
```