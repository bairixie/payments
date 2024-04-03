"""
Web Steps

Steps file for web interactions with Selenium framework
"""
# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions


ID_PREFIX = "payments_"

@when('I visit the "Home Page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)

@then('I should see "{message}" in the title')
def step_impl(context, message):
    """Check the title for a message"""
    assert message in context.driver.title

@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    element = context.driver.find_element(By.TAG_NAME, 'body')
    assert text_string not in element.text

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower().replace(" ", "-")
    context.driver.find_element(By.ID, button_id).click()

@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'results-body'),
            name
        )
    )
    assert found

@when('I set the "{element_name}" to "{value}"')
def step_impl(context, element_name, value):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(value)

@then('I should see the "{notification_type}" notification')
def step_impl(context, notification_type):
    css_selector_name = f'div.notification.{notification_type.lower()}'
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, css_selector_name))
    )
    assert found

@when('I copy the "{element_name}"')
def step_impl(context, element_name):
    element_id = element_name.lower().replace(" ", "-")
    element = context.driver.find_element(By.ID, element_id)
    context.clipboard = element.text
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste to "{element_name}"')
def step_impl(context, element_name):
    element_id = element_name.lower().replace(" ", "-")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = element_name.lower()
    element = Select(context.driver.find_element(By.ID, element_id))
    element.select_by_visible_text(text)
@when('I press the "Delete" button for "{payment_method_name}"')
def step_impl(context, payment_method_name):
    # Assuming each payment method is associated with a unique delete button identified by its name
    delete_button_id = f"{ID_PREFIX}{payment_method_name.lower().replace(' ', '-')}-delete-btn"
    context.driver.find_element(By.ID, delete_button_id).click()

@then('a confirmation popup should appear')
def step_impl(context):
    # Assuming a confirmation popup appears with a specific identifier upon clicking delete
    confirmation_popup_class = 'confirmation-popup'
    WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.visibility_of_element_located((By.CLASS_NAME, confirmation_popup_class))
    )

@when('I confirm deletion in the popup')
def step_impl(context):
    # Assuming the confirmation popup has a confirm button to proceed with the deletion
    confirm_button_id = 'confirm-delete'
    context.driver.find_element(By.ID, confirm_button_id).click()

@then('"{payment_method_name}" should no longer be present in the list')
def step_impl(context, payment_method_name):
    # This checks if the payment method has been successfully removed by confirming its absence
    try:
        WebDriverWait(context.driver, 3).until_not(
            expected_conditions.text_to_be_present_in_element(
                (By.ID, "results-body"), payment_method_name)
        )
    except TimeoutException:
        # If TimeoutException is caught, it means the element is still present after waiting
        assert False, f"{payment_method_name} is still present after attempting deletion."


