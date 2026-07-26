# Domain Model

## General Model

```plantuml
/' Global model with all major concepts and cross-subdomain relationships here. '/
```

## Workflow Trace

1. Conceptual classes identified
2. UML classes drawn
3. Associations and attributes added

## Sub-domain Diagrams

<!-- for large domains, this section MUST come after General Model -->

<!-- mandatory when the domain is split into sub-domains; one diagram per sub-domain -->
{for sub-domain in sub-domains}
# Sub-domain {{sub-domain-name}}
```plantuml
/' Keep local classes inside {{sub-domain-name}} package. '/
/' Cross-sub-domain associations must be outside the package. '/
/' External classes must use prefix with line break before dot: '/
/' OtherSubdomain '/
/' .ClassName '/
```
{end sub-domain}

## Validation Checklist

- [ ] Both discovery techniques used (category list + noun phrases)
- [ ] No software classes or methods in diagrams
- [ ] Out-of-scope concepts excluded
- [ ] If large domain: General Model is present in first section
- [ ] One diagram per sub-domain (if large domain, after General Model)
- [ ] Cross-sub-domain associations outside local package
- [ ] External class references follow:

```text
OtherSubdomain
.ClassName
```