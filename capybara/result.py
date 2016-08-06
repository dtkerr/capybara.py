from capybara.helpers import failure_message


class Result(object):
    """
    A :class:`Result` represents a collection of :class:`Element` objects on the page. It is
    possible to interact with this collection similar to a List because it implements
    ``__getitem__`` and offers the following container methods through delegation:

    * ``__len__``
    * ``__nonzero__`` (Python 2)

    Args:
        elements (List[Element]): The list of elements found by the query.
        query (SelectorQuery): The query used to find elements.
    """

    def __init__(self, elements, query):
        self.result = elements
        self.query = query

    def __getitem__(self, key):
        return self.result[key]

    def __len__(self):
        return len(self.result)

    def __nonzero__(self):
        return len(self.result) > 0

    @property
    def failure_message(self):
        """ str: A message describing the query failure. """
        message = failure_message(self.query.description)
        message += " but there were no matches"
        return message