# Customer Questions

## Shared Teacher Generation Key

**Decision source:** [DEC-018](decisions.md#dec-018) permits the administrator
to provide a shared generation key that teachers may use. The product must never
show or export that secret value to teachers, students or logs.

Please decide:

1. Which provider and credential format does the shared key use?
2. Where may the product store it: an external secret manager, encrypted
   application storage, or deployment-only configuration?
3. Who may replace or revoke it, and what should teachers see when it is absent,
   revoked or exhausted?
4. What usage, quota and rotation information may administrators and teachers
   see?

## Teacher Email Policy

**Decision source:** [DEC-019](decisions.md#dec-019) requires university-email
authorization, while the current team direction permits an administrator to
create teacher accounts with any email address.

Please confirm whether the university-email restriction applies to teacher
accounts. If it does, provide the accepted domain list and verification method.
