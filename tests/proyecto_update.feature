Feature: Update proyect

Scenario: The project is edited successfully
    Given the user has alredy created a project
    And the user declares one or more project data
    When the user chooses to apply the changes to the project
    Then the new data is established and the user is informed

Scenario: Nulling a required field
    Given the user has alredy created a project
    And the user deletes one or more required data and leaves them without information
    When the user chooses to apply the changes to the project
    Then the user is  informed that it is not possible to apply the changes because there is missing data and is asked to complete them to edit the project
    