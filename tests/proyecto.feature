Feature: Create proyect

  Scenario: The project is created successfully
    Given the user declares the mandatory project data
    When the user chooses to confirm the creation of the project
    Then the project is created with the previously loaded data and the user is informed
