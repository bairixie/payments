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
    # Assuming each delete button has an ID like "delete-payment_method_name"
    delete_button_id = f"delete-{payment_method_name.lower().replace(' ', '-')}"
    context.driver.find_element(By.ID, delete_button_id).click()

@then('a confirmation popup should appear')
def step_impl(context):
    # Wait for the confirmation popup to be visible
    WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.visibility_of_element_located((By.ID, "confirmation-popup"))
    )

@when('I confirm deletion in the popup')
def step_impl(context):
    # Click the confirmation button within the popup
    context.driver.find_element(By.ID, "confirm-delete").click()

@then('"{payment_method_name}" should no longer be present in the list')
def step_impl(context, payment_method_name):
    # Refresh the list or navigate to ensure the list is updated
    context.driver.get(context.base_url + "/path-to-refresh-list")

    # Verify the payment method is not present
    page_source = context.driver.page_source
    assert payment_method_name not in page_source, f"{payment_method_name} is still present after deletion."

@given('I have added a PayPal payment method with the following details')
def step_impl(context):
    # This step can be implemented by directly interacting with the UI to add a PayPal payment method
    # or by making an API call to add a PayPal payment method in the setup stage.
    raise NotImplementedError(u'STEP: Given I have added a PayPal payment method with the following details')

@given('I have added a Credit Card payment method with the following details')
def step_impl(context):
    # Similar to the PayPal step, implement the addition of a Credit Card payment method.
    raise NotImplementedError(u'STEP: Given I have added a Credit Card payment method with the following details')

@when('a confirmation popup should appear')
def step_impl(context):
    # Verify the confirmation popup's appearance, which might involve waiting for a popup element to be visible.
    raise NotImplementedError(u'STEP: When a confirmation popup should appear')

@then('"{payment_method_name}" should no longer be present in the list')
def step_impl(context, payment_method_name):
    # Verify the payment method is not listed, potentially by asserting the absence of the payment method name in the results.
    raise NotImplementedError(u'STEP: Then "{payment_method_name}" should no longer be present in the list')


