#!/usr/bin/python3
# -*-coding:Utf-8 -*

import notifier

# print('Username:')
# username = input()
# print('Password:')
# password = input()

configs = [{
	'category': 'mk',
	'url': 'http://www.markknopfler.com/news',
	'articleSelector': 'article.post',
	'titleSelector': 'h3',
	'linkSelector': 'h3 a',
	'bodySelector': 'p + p',
	'logFile': '/Users/nathan/sandbox/Notifier/logs/log.mk'
}, {
	'category': 'sog',
	'url': 'http://www.secretsofgrindea.com/index.php/dev-blog',
	'articleSelector': '#posts div.post',
	'titleSelector': 'div.header',
	'linkSelector': 'div.header a',
	'bodySelector': 'div.post-content div.edited-content',
	'logFile': '/Users/nathan/sandbox/Notifier/logs/log.sog'
}, {
	'category': 'sog',
	'url': 'https://twitter.com/hashtag/SecretsofGrindea?src=hash&lang=en',
	'articleSelector': 'div.stream ol li.stream-item div.tweet div.content',
	'titleSelector': 'div.js-tweet-text-container p',
	'linkSelector': 'div.js-tweet-text-container p a',
	'bodySelector': None,
	'logFile': '/Users/nathan/sandbox/Notifier/logs/log.tweeter.sog'
}, {
	'category': 'lh',
	'url': 'https://twitter.com/lifehacker',
	'articleSelector': 'div.stream ol li.stream-item div.tweet div.content',
	'titleSelector': 'div.js-tweet-text-container p',
	'linkSelector': 'div.js-tweet-text-container p a',
	'bodySelector': None,
	'logFile': '/Users/nathan/sandbox/Notifier/logs/log.tweeter.lh'
}]

for conf in configs:
	try:
		nc = notifier.NewsCrawler(conf)
		tracker = notifier.NewsTracker(nc, conf['category'], conf['logFile'])
		tracker.watch(90)
	except Exception as exc:
		print('watch script, exception occured: '+str(exc))
