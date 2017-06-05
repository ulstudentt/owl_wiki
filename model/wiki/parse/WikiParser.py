import re


class WikiParser:
    """
    Класс, предоставляющий информацию из mediaWiki.

    get_category_pages() - возвращает словарь категорий
    :key - имя категории
    :item - имена родительских категорий

    get_instance_pages() - возвращает список страниц mediaWiki
    """
    category_text = "Category:"

    def __init__(self, wiki_connector):
        self.wiki_connector = wiki_connector
        self.site = self.connector.get_logged_site()

    def get_category_pages(self):
        categories_pages = self.site.categories
        category_pages_and_parents = {}
        for category_page in categories_pages:
            category_pages_and_parents[category_page.page_title] = (category_page, [])
            page_text = category_page.text()
            search_res = re.findall(r'\[\[(' + self.category_text + ')(.*?)]]', page_text)

            for occurrence in search_res:
                category_pages_and_parents[category_page.page_title][1].append(occurrence[1])
        return category_pages_and_parents

    def get_instance_pages(self):
        return self.site.pages
