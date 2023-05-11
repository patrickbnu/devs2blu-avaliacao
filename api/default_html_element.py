from typing import Dict, List

from lxml.html import HtmlElement, FormElement


class DefaultHtmlElement(HtmlElement):

    text = ""

    def __init__(self):
        super(DefaultHtmlElement, self).__init__(self)
        self._json = {}

    def content(self) -> str:
        """
        Return the element content as a string
        :return:
        """
        text = self.text_content()
        return (text or "").strip()

    def first(self, path) -> HtmlElement:
        """
        Return the first element from a list of elements
        :param path: xpath ./div/a[@class="first"]
        :return: lxml HTML element monkey patched with our custom functions
        """
        from api.xpath_utils import map_lxml_html_to_custom_html_element

        elements = self.xpath(path)
        if not elements:
            # Return a default HTML element - it won't have any content
            element = map_lxml_html_to_custom_html_element(HtmlElement())
            element.empty = True
            return element
        return map_lxml_html_to_custom_html_element(elements[0])

    def last(self, path) -> HtmlElement:
        """
        Return the last element in a list of elements
        :param path: xpath ./div/a[@class="first"]
        :return: lxml HTML element monkey patched with our custom functions
        """
        from api.xpath_utils import map_lxml_html_to_custom_html_element

        elements = self.xpath(path)
        if not elements:
            # Return a default HTML element - it won't have any content
            element = map_lxml_html_to_custom_html_element(HtmlElement())
            element.empty = True
            return element
        return map_lxml_html_to_custom_html_element(elements[-1])

    def elements(self, _path) -> List:
        """
        Return a list of elements matching the xpath selection
        :param _path: xpath ./div/a[@class="first"]
        :return:
        """
        from api.xpath_utils import map_lxml_html_to_custom_html_element

        elements = self.xpath(_path)
        return [map_lxml_html_to_custom_html_element(element) for element in elements]

    def json(self) -> Dict:
        """
        Return the JSON styled content if applicable
        """
        if hasattr(self, "_json"):
            return self._json
        return {}

    def data(self) -> Dict:
        data_dict = {}
        if self.__class__ != FormElement:
            return {}
        inputs = self.xpath(".//input")
        for form_input in inputs:
            data_dict[form_input.name] = form_input.value
        return data_dict
