# UC00 <Title, starts with a verb>

[Use Case Model](../Use%20Case%20Model.md)

## Goal
<One sentence goal>

```plantuml
/' uml state diagram of the use case '/
```

## Scope
<The system under design>

## Level
<User goal | Sub-function>

## Priary actor
<Calls on the system to deliver its services>

## Stakeholders and Interests
<Who cares about this use case, and what do they want?>

## Preconditions
<What must be true on start, and worth telling the reader?>

## Success guarantee
<What must be true on successfull completion, and worth telling the reader>

## Main Success Scenario 
<!-- A typical, unconditional happy path scenario of success, approximately 5 to 10 steps -->
{for step in steps}
{{#}}. {{step}}
{end step}

## Extensions (or Alternate flows)

{for extension in extensions}
- step {{#}}{{''|letter}}. {{condition | response}}
{end extension}

## Special requirements
<Related non ¡-functional requirements>

## Technology and Data Variations List
<Varying I-O methods and data formats>

## Frequency of Occurrence
<Influences investigation, testing, and timing of implementation>

## Miscellaneous
<Such as open issues>
