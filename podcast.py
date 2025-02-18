#!/usr/bin/env python3

import os
import datetime
import pydub
import re

def main():
    base = "https://wctang-data.github.io/bettywu-jinpingmei"
    name = "金瓶梅"
    _now = datetime.datetime.now()

    rex = re.compile(r'\d+_(.*)\.mp3')

    with open("feed.xml", "w", encoding="utf-8", newline='\n') as out:
        print(f'''<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
<channel>
<title>{name}</title>
<description>{name}</description>
<itunes:image href="{base}/logo.jpg"/>
<link>{base}/</link>
<language/>
<pubDate>{_now}</pubDate>
<author>wctang-data</author>''', file=out)

        idx = 0
        for dirpath, _, filenames in os.walk("."):
            dirpath = dirpath[2:]
            if dirpath.startswith(".git"):
                continue
            for filename in filenames:
                if not (m := rex.match(filename)):
                    continue
                info = pydub.utils.mediainfo(f'{filename}')
                print(f'<item><title>{m[1]}</title><pubDate>{_now+datetime.timedelta(seconds=idx)}</pubDate><enclosure url="{base}/{filename}" type="audio/mpeg" length="{info["size"]}"/><itunes:duration>{int(float(info["duration"]))}</itunes:duration></item>', file=out)
                idx += 1

        print('''</channel>
</rss>''', file=out)


if __name__ == '__main__':
    main()
