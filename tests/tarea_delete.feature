Scenario: Task is deleted successfully
    Given there are tasks created within a project
    When the user chooses to delete a task
    And confirm the deletion of the task
    Then the task is deleted and is no longer shown in the project task list
