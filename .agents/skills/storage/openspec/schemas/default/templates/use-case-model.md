# Use Case Model

```plantuml
/' Use cases diagram in plantuml grammar '/
```

## Use cases

{for use-case in use-cases}
- [{{use case name}}](./use-cases/{{relative path to use case markdown file using `%20` for empty espaces}})
    - System Sequence Diagrams:
        {for ssd in use-case-related-ssds}
        - [{{ssd name}}](./SSDs/{{relative path to ssd `%20` for empty espaces}})
        {end ssd}
    - Operation Contracts:
        {for operation-contract in use-case-related-operation-contracts}
        - [{{operation-contract name}}](./Operation%20Contracts/{{relative path to operation-contract `%20` for empty espaces}})
        {end operation-contract}
{end use-case}