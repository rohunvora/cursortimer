---
name: CI Pipeline Failure
about: Report a CI pipeline failure or flaky test
title: '[CI] '
labels: 'ci/cd, bug'
assignees: ''
---

## CI Failure Details

**Workflow Run**: [Link to failed workflow run]

**Job that failed**: 
- [ ] Pre-commit checks
- [ ] Python tests
- [ ] Python linting
- [ ] TypeScript checks
- [ ] Integration tests
- [ ] Build artifacts
- [ ] Coverage report

**Python version** (if applicable): 
**OS** (if applicable): 

## Error Message

```
Paste the relevant error message here
```

## Steps to Reproduce (if applicable)

1. 
2. 
3. 

## Expected Behavior

Describe what should happen

## Additional Context

- Is this a flaky test? (fails sometimes but not always)
- Did this start after a specific commit?
- Any recent dependency updates?

## Checklist

- [ ] I've checked if this is already reported
- [ ] I've tried running the test locally
- [ ] I've checked the CI configuration hasn't changed