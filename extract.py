#!/usr/bin/env python
from functools import lru_cache

import lxml.html
from lxml import etree


@lru_cache(5)
def extract_html(page):
    return lxml.html.fromstring(page)


def extract_content(page):
    success = False
    root = extract_html(page.text)
    try:
        form = root.xpath("//form")[0]
        payload = {elt.name: elt.value for elt in form.inputs if elt.name is not None}
    except IndexError:
        payload = {"level": 3}
        success_list = root.xpath("//p[@class='day-success']")
        if len(success_list):
            success_message = success_list[0].text_content()
            success = True
    level = int(payload["level"])
    position = level - 1 if level < 3 else 0
    articles = root.xpath("//article")
    content = [etree.tostring(article).decode() for article in articles]
    result = {"content": content, "level": level, "payload": payload, "position": position}
    if success:
        result["success"] = success_message
    return result, page.text
