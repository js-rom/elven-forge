---
name: {{directory name}}
description: {{description}}
license: MIT
metadata:
  author: js-rom
  version: "1.0"
---

# Purpose

{{purpose}}

# What you receive

{{receivable input}}

# What you need to do

```md
{{ for step in steps }}
## Step `{{ # }}`: {{ step_description }}
{{ end step }}
```

## Anti-Patterns

```md
{{ for santi_pattern in santi_patterns }}
- {{ santi_pattern_description }}
{{ end santi_pattern }}
```

# Results

