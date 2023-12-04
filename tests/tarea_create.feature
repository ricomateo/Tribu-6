Scenario: Task is created successfully
    Given the user declares the required task data
    When the user chooses to confirm the creation of the task
    Then the task is added to the project successfully and the user is informed

Scenario: Missing data
    Given the user omits at least one of the required task data
    When the user chooses to confirm the creation of the task
    Then the user is informed that there is missing data and is prompted to complete it to successfully create the task

Scenario: A task with that name already exists
    Given the user declares the required task data
    And the declared name is the same as the name of an existing task in the project
    When the user chooses to confirm the creation of the task
    Then the task is added to the project successfully and the user is informed