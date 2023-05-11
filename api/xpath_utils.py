import types

from lxml import html
from lxml.html import HtmlElement
from requests import Response

from api.default_html_element import DefaultHtmlElement


def map_lxml_html_to_custom_html_element(element: HtmlElement) -> HtmlElement:
    custom_functions = set(dir(DefaultHtmlElement))
    existing_functions = set(dir(element))
    for func in custom_functions:
        if func not in existing_functions and callable(
            getattr(DefaultHtmlElement, func)
        ):
            element.__dict__[
                getattr(DefaultHtmlElement, func).__name__
            ] = types.MethodType(getattr(DefaultHtmlElement, func), element)
    setattr(element, "empty", False)
    return element


def bind_custom_html_element(raw_html: Response) -> HtmlElement:
    if not raw_html.content:
        element = HtmlElement()
    else:
        element = html.fromstring(raw_html.content)
    element.status_code = raw_html.status_code
    element.url = raw_html.url
    element.headers = raw_html.headers
    element.content = raw_html.content
    element.text = raw_html.text
    try:
        element._json = raw_html.json()
    except Exception:
        element._json = {}

    return map_lxml_html_to_custom_html_element(element)
