Feature: The payments service back-end
    As an e-commerce platform owner
    I need a RESTful service for payments
    So that my platform's users can create payment methods

Background:
    Given the following payment methods
        | name        | user_id | type        | email             | first_name | last_name | card_number      | expiry_month | expiry_year | security_code | billing_address | zip_code |
        | best method | 1       | PAYPAL      | testmail@mail.com |            |           |                  |              |             |               |                 |          |
        | do not use  | 90      | PAYPAL      | john.doe@mail.com |            |           |                  |              |             |               |                 |          |
        | secondary   | 1130    | PAYPAL      | jane.doe@mail.com |            |           |                  |              |             |               |                 |          |
        | abc         | 1       | CREDIT_CARD |                   | john       | doe       | 1234123412341234 | 11           | 2027        | 123           | 90 W East St    | 10001    |
        | efg         | 1       | CREDIT_CARD |                   | john       | doe       | 3456345634563456 | 06           | 2026        | 999           | 10 W East St    | 10003    |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Payments" in the title
    And I should not see "404 Not Found"

Scenario: Create a PayPal payment method
    When I visit the "Home Page"
    And I press the "Create new Payment Method" button
    And I set the "Name" to "new payment method"
    And I set the "User ID" to "12"
    And I set the "Email" to "test@gmail.com"
    And I press the "Dialog Form Submit" button
    Then I should see the "Success" notification
    When I copy the "Notification Payment Method ID"
    And I paste to "Retrieve Payment Method ID"
    And I press the "Retrieve Payment Method" button
    Then I should see "new payment method" in the results

Scenario: Create a Credit Card payment method
    When I visit the "Home Page"
    And I press the "Create new Payment Method" button
    And I set the "Name" to "yet another credit card"
    And I set the "User ID" to "100"
    And I select "Credit Card" in the "Type" dropdown
    And I set the "First Name" to "John"
    And I set the "Last Name" to "Doe"
    And I set the "Card Number" to "12341234"
    And I set the "Expiry Month" to "10"
    And I set the "Expiry Year" to "2025"
    And I set the "Security Code" to "776"
    And I set the "Billing Address" to "120 W 3rd St"
    And I set the "Zip Code" to "11008"
    And I press the "Dialog Form Submit" button
    Then I should see the "Error" notification
    When I set the "Card Number" to "1234123412341234"
    And I press the "Dialog Form Submit" button
    Then I should see the "Success" notification
    When I copy the "Notification Payment Method ID"
    And I paste to "Retrieve Payment Method ID"
    And I press the "Retrieve Payment Method" button
    Then I should see "yet another credit card" in the results

Scenario: Delete a Payment Method
    Given I have added a payment method with the following details
        | name           | user_id | type        | email              | first_name | last_name | card_number       | expiry_month | expiry_year | security_code | billing_address | zip_code |
        | disposable one | 99      | CREDIT_CARD | dispose-me@mail.com| John       | Disposable| 5555444433331111  | 12           | 2030        | 456           | 123 Dispose St  | 99999    |
    When I visit the "Home Page"
    And I press the "Search Payment Methods" button
    Then I should see "disposable one" in the results
    When I press the "Delete" button for "disposable one"
    And a confirmation popup should appear
    And I confirm deletion in the popup
    Then "disposable one" should no longer be present in the list



Scenario: List all payment methods
    When I visit the "Home Page"
    And I press the "Search Payment Methods" button
    Then I should see "best method" in the results
    And I should see "do not use" in the results
    And I should see "secondary" in the results
    And I should see "abc" in the results
    And I should see "efg" in the results
