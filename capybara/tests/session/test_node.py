import pytest
from time import sleep

import capybara
from capybara.tests.helpers import extract_results


class NodeTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")


class TestNode(NodeTestCase):
    def test_acts_like_a_session_object(self, session):
        session.visit("/form")
        form = session.find("css", "#get-form")
        assert form.has_field("Middle Name")
        form.fill_in("Middle Name", value="Monkey")
        form.click_button("med")
        assert extract_results(session)["form[middle_name]"] == "Monkey"

    def test_scopes_css_selectors(self, session):
        assert not session.find("css", "#second").has_css("h1")


class TestNodeQueryScope(NodeTestCase):
    def test_returns_a_reference_to_the_element_the_query_was_evaluated_on(self, session):
        node = session.find("css", "#first")
        assert node.query_scope == node.session.document
        assert node.find("css", "#foo").query_scope == node


class TestNodeText(NodeTestCase):
    def test_extracts_node_text(self, session):
        assert session.find_all("//a")[0].text == "labore"
        assert session.find_all("//a")[1].text == "ullamco"

    def test_returns_document_text_on_html_selector(self, session):
        session.visit("/with_simple_html")
        assert session.find("/html").text == "Bar"


class TestNodeAttribute(NodeTestCase):
    def test_extracts_node_attributes(self, session):
        assert session.find_all("//a")[0]["class"] == "simple"
        assert session.find_all("//a")[1]["id"] == "foo"
        assert session.find_all("//input")[0]["type"] == "text"

    def test_extracts_boolean_node_attributes(self, session):
        assert session.find("//input[@id='checked_field']")["checked"]


class TestNodeValue(NodeTestCase):
    def test_allows_retrieval_of_the_value(self, session):
        assert session.find("//textarea[@id='normal']").value == "banana"

    def test_does_not_swallow_extra_newlines_in_textarea(self, session):
        assert session.find("//textarea[@id='additional_newline']").value == "\nbanana"

    def test_does_not_swallow_newlines_for_set_content_in_textarea(self, session):
        session.find("//textarea[@id='normal']").set("\nbanana")
        assert session.find("//textarea[@id='normal']").value == "\nbanana"

    def test_returns_any_html_content_in_textarea(self, session):
        session.find("//textarea[1]").set("some <em>html</em>here")
        assert session.find("//textarea[1]").value == "some <em>html</em>here"

    def test_defaults_to_on_for_checkboxes(self, session):
        session.visit("/form")
        assert session.find("//input[@id='valueless_checkbox']").value == "on"

    def test_defaults_to_on_for_radio_buttons(self, session):
        session.visit("/form")
        assert session.find("//input[@id='valueless_radio']").value == "on"


class TestNodeSet(NodeTestCase):
    def test_allows_assignment_of_field_value(self, session):
        assert session.find_first("//input").value == "monkey"
        session.find_first("//input").set("gorilla")
        assert session.find_first("//input").value == "gorilla"


class TestNodeTagName(NodeTestCase):
    def test_extracts_node_tag_name(self, session):
        assert session.find_all("//a")[0].tag_name == "a"
        assert session.find_all("//a")[1].tag_name == "a"
        assert session.find_all("//p")[0].tag_name == "p"


class TestNodeDisabled(NodeTestCase):
    def test_extracts_disabled_node(self, session):
        session.visit("/form")
        assert session.find("//input[@id='customer_name']").disabled
        assert not session.find("//input[@id='customer_email']").disabled

    def test_sees_disabled_options_as_disabled(self, session):
        session.visit("/form")
        assert not session.find("//select[@id='form_title']/option[1]").disabled
        assert session.find("//select[@id='form_title']/option[@disabled]").disabled

    def test_sees_enabled_options_in_disabled_select_as_disabled(self, session):
        session.visit("/form")
        assert session.find("//select[@id='form_disabled_select']/option").disabled
        assert not session.find("//select[@id='form_title']/option[1]").disabled

    def test_is_boolean(self, session):
        session.visit("/form")
        assert session.find("//select[@id='form_disabled_select']/option").disabled is True
        assert session.find("//select[@id='form_disabled_select2']/option").disabled is True
        assert session.find("//select[@id='form_title']/option[1]").disabled is False


class TestNodeChecked(NodeTestCase):
    def test_extracts_node_checked_state(self, session):
        session.visit("/form")
        assert session.find("//input[@id='gender_female']").checked is True
        assert session.find("//input[@id='gender_male']").checked is False
        assert session.find_first("//h1").checked is False


class TestNodeSelected(NodeTestCase):
    def test_extracts_node_selected_state(self, session):
        session.visit("/form")
        assert session.find("//option[@value='en']").selected is True
        assert session.find("//option[@value='sv']").selected is False
        assert session.find_first("//h1").checked is False


class TestNodeEquals(NodeTestCase):
    def test_is_true_for_the_same_element(self, session):
        assert session.find("//h1") == session.find("//h1")

    def test_is_false_for_different_elements(self, session):
        assert session.find("//h1") != session.find_first("//p")

    def test_is_false_for_unrelated_objects(self, session):
        assert session.find("//h1") != "Not a node"


class TestNodeReloadWithoutAutomaticReload(NodeTestCase):
    @pytest.fixture(autouse=True)
    def setup_capybara(self):
        capybara.automatic_reload = False

    def test_reloads_the_current_context_of_the_node(self, session):
        session.visit("/with_js")
        node = session.find("css", "#reload-me")
        session.click_link("Reload!")
        sleep(0.3)
        assert node.reload().text == "has been reloaded"
        assert node.text == "has been reloaded"

    def test_reloads_a_parent_node(self, session):
        session.visit("/with_js")
        node = session.find("css", "#reload-me").find("css", "em")
        session.click_link("Reload!")
        sleep(0.3)
        assert node.reload().text == "has been reloaded"
        assert node.text == "has been reloaded"

    def test_does_not_automatically_reload(self, session):
        session.visit("/with_js")
        node = session.find("css", "#reload-me")
        session.click_link("Reload!")
        sleep(0.3)
        with pytest.raises(Exception) as excinfo:
            assert node.has_text("has been reloaded")
        assert isinstance(excinfo.value, session.driver.invalid_element_errors)


class TestNodeReloadWithAutomaticReload(NodeTestCase):
    @pytest.fixture(autouse=True)
    def setup_capybara(self):
        capybara.automatic_reload = True

    def test_reloads_the_current_context_of_the_node_automatically(self, session):
        session.visit("/with_js")
        node = session.find("css", "#reload-me")
        session.click_link("Reload!")
        sleep(0.3)
        assert node.text == "has been reloaded"

    def test_reloads_a_parent_node_automatically(self, session):
        session.visit("/with_js")
        node = session.find("css", "#reload-me").find("css", "em")
        session.click_link("Reload!")
        sleep(0.3)
        assert node.text == "has been reloaded"

    def test_reloads_a_node_automatically_when_using_find(self, session):
        session.visit("/with_js")
        node = session.find("css", "#reload-me")
        session.click_link("Reload!")
        sleep(0.3)
        assert node.find("css", "a").text == "has been reloaded"

    def test_does_not_reload_nodes_which_have_not_been_found_with_reevaluatable_queries(self, session):
        session.visit("/with_js")
        node = session.find_all("css", "#the-list li")[1]
        session.click_link("Fetch new list!")
        sleep(0.3)
        with pytest.raises(Exception) as excinfo:
            assert node.has_text("Foo")
        assert isinstance(excinfo.value, session.driver.invalid_element_errors)
        with pytest.raises(Exception) as excinfo:
            assert node.has_text("Bar")
        assert isinstance(excinfo.value, session.driver.invalid_element_errors)
