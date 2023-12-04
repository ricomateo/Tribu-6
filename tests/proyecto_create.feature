Feature: Create proyect

Scenario: The project is created successfully
    Given the user declares the mandatory project data
    When the user chooses to confirm the creation of the project
    Then the project is created with the previously loaded data and the user is informed

Scenario: Missing data
    Given the user omits at least one of the project's required data
    When the user chooses to confirm the creation of the project
    Then the user is informed that there is missing data and is asked to complete it to successfully create the project

Scenario: A project with the same name already exists
    Given the user declares the mandatory project data
    And the declared name is the same as the name of an existing project
    When the user chooses to confirm the creation of the project
    Then the project is created with the previously loaded data and the user is informed

Scenario: Wrong proyect leader id
    Given the user declares the wrong project leader id
    When the user chooses to confirm the creation of the project
    Then the user is informed that there is no employee with that id and is asked to correct it to successfully create the project