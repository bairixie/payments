"""
Web Steps
Steps file for web interactions with Selenium framework
"""
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from behave import when, then

ID_PREFIX = "payments_"

@when('I visit the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)

@then('I should see "{message}" in the title')
def step_impl(context, message):
    assert message in context.driver.title, f"Expected title '{message}' not found in the current title '{context.driver.title}'"

@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    body_text = context.driver.find_element(By.TAG_NAME, 'body').text
    assert text_string not in body_text, f"Found text '{text_string}' in the page body."

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = f"{ID_PREFIX}{button.lower().replace(' ', '-')}"
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, button_id))
    ).click()

@then('I should see "{name}" in the results')
def step_impl(context, name):
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, 'results-body'), name),
        f"Payment method '{name}' was not found in the results."
    )

@when('I set the "{element_name}" to "{value}"')
def step_impl(context, element_name, value):
    element_id = f"{ID_PREFIX}{element_name.lower().replace(' ', '_')}"
    input_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    input_field.clear()
    input_field.send_keys(value)

@then('I should see the "{notification_type}" notification')
def step_impl(context, notification_type):
    notification_xpath = f"//div[contains(@class, 'notification') and contains(@class, '{notification_type.lower()}')]"
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, notification_xpath)),
        f"Expected notification of type '{notification_type}' not found."
    )

@when('I copy the "{element_name}"')
def step_impl(context, element_name):
    element_id = f"{ID_PREFIX}{element_name.lower().replace(' ', '-')}"
    element_text = context.driver.find_element(By.ID, element_id).text
    context.clipboard = element_text
    logging.info(f"Clipboard contains: {context.clipboard}")

@when('I paste to "{element_name}"')
def step_impl(context, element_name):
    element_id = f"{ID_PREFIX}{element_name.lower().replace(' ', '-')}"
    target_element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    target_element.clear()
    target_element.send_keys(context.clipboard)

@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = f"{ID_PREFIX}{element_name.lower()}"
    select_element = Select(WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, element_id))
    ))
    select_element.select_by_visible_text(text)

@when('I press the "Delete" button for "{payment_method_name}"')
def step_impl(context, payment_method_name):
    delete_button_id = f"{ID_PREFIX}{payment_method_name.lower().replace(' ', '-')}-delete"
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, delete_button_id))
    ).click()

@then('a confirmation popup should appear')
def step_impl(context):
    # Assuming the application has a common class for confirmation popups
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "confirmation-popup")),
        "Confirmation popup did not appear as expected."
    )

@when('I confirm deletion in the popup')
def step_impl(context):
    confirm_button_id = 'confirm-delete'
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, confirm_button_id))
    ).click()

@then('"{payment_method_name}" should no longer be present in the list')
def step_impl(context, payment_method_name):
    try:
        WebDriverWait(context.driver, 3).until_not(
            EC.text_to_be_present_in_element((By.ID, "results-body"), payment_method_name)
        )
    except TimeoutException:
        assert False, f"{payment_method_name} is still present after attempting deletion."


