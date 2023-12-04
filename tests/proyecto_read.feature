Feature: Read proyect

Scenario: There are projects
    Given there are projects created
    When the user chooses to consult the projects
    Then you are shown a list of all the projects

Scenario: No projects created
    Given there are no projects created
    When the user chooses to consult the projects
    Then you are informed that there are no projects yet