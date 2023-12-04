Scenario: The task is edited successfully
    Given there are already projects and tasks created
    And the user declares one or more task data 
    When the user chooses to apply the changes
    Then the new data is established and the user is informed

Scenario: Nulling a required field
    Given there are already projects and tasks created
    And the user deletes one or more mandatory data from the task and leaves them without information
    When the user chooses to apply the changes
    Then the user is informed that the changes cannot be applied because there is missing data and is asked to complete them to edit the task 