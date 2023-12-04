Scenario: Tasks are displayed successfully
    Given the project has tasks
    When the user chooses to consult the project tasks
    Then you are shown a list of all the tasks

Scenario: No tasks to display
    Given the project has no tasks
    When the user chooses to consult the project tasks
    Then you are informed that the project has no tasks