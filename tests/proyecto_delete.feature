Scenario: The project is successfully deleted
    Given there are projects created
    When the user chooses to delete a project
    And confirm the deletion of the project
    Then the project is deleted and is no longer shown in the project list