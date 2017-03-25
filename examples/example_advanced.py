#!/usr/bin/python3
# -*- coding: utf-8 -*-
import serpscrap

keywords = ['news']

config = serpscrap.Config()

config.set('scrape_urls', True)
config.set('num_pages_for_keyword', 2)
config.set('url_threads', 5)

scrap = serpscrap.SerpScrap()
scrap.init(config=config.get(), keywords=keywords)
results = scrap.run()

markovi = serpscrap.Markovi(config)

models = []

for result in results:
    if 'serp_title' in result and len(result['serp_title']) > 1:
        model = markovi.get_model(result['serp_title'], 1)
        if model.state_size > 0:
            models.append(model)

model = markovi.get_combined_model(models)

texts = []
for _ in range(len(results)):
    text = model.make_sentence(
        char_limit=150,
        tries=10,
        max_overlap_ratio=0.7,
        max_overlap_total=25
    )
    if isinstance(text, str):
        texts.append(text)

for text in texts:
    print(text+'\n')

tf = serpscrap.TfIdf().get_tfidf(texts)
print(tf[0:10])

model = markovi.get_model("\n".join(texts), 1)
for _ in range(10):
    text = model.make_short_sentence(
        char_limit=80,
        tries=10,
        max_overlap_ratio=0.7,
        max_overlap_total=20
    )
    if text is not None:
        print(text)
