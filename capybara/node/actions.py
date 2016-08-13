class ActionsMixin(object):
    """
    If the driver is capable of executing JavaScript, actions will wait for a set amount of time and
    continuously retry finding the element until either the element is found or the time expires.
    The length of time :meth:`find` will wait is controlled through
    :data:`capybara.default_max_wait_time`.
    """

    def click_button(self, locator, **kwargs):
        """
        Finds a button on the page and clicks it. This can be any ``<input>`` element of type
        submit, reset, image, or button, or it can be any ``<button>`` element. All buttons can be
        found by their id, value, or title. ``<button>`` elements can also be found by their text
        content, and image ``<input>`` elements by their alt attribute.

        Args:
            locator (str): Which button to find.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        return self.find("button", locator, **kwargs).click()

    def click_link(self, locator, **kwargs):
        """
        Finds a link by id, text, or title and clicks it. Also looks at image alt text inside the
        link.

        Args:
            locator (str): Text, id, title, or nested image's alt attribute.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        return self.find("link", locator, **kwargs).click()
