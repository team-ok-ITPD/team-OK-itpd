# REL-09 release preparation

This is a release-owner checklist, not a published release or authorization to
bypass independent review. No tag or released changelog section is created here.

## Build Boundaries

- Review: the owner reports `main` at 13:30 on 28 November. The
  [candidate baseline](../../docs/user-acceptance-tests.md#review-baseline)
  is qualified by timezone and deployment verification.
- Same-sprint rework: administrator corrections in
  [#220](https://github.com/team-ok-ITPD/team-OK-itpd/pull/220) are a separate,
  later build. The release owner decides what reviewed/merged work is included.
- Release: choose a full merged product commit after required review and checks.
  Never label the meeting baseline as testing later rework.
- Submission: the later main commit including the merged report/evidence may
  differ from the product tag; its permalink and ZIP must match each other.

## Before Tagging

- [ ] Verify selected PRs have independent approval and are merged to main.
- [ ] Verify the exact product commit and its CI checks, not an arbitrary branch.
- [ ] Confirm the actual UAT results, quality checks and known limitations.
- [ ] Select the next SemVer version from the live release/tag history.
- [ ] Confirm deployment owner and apply any migrations. The administrator
  change adds `core.0013_studygroup_is_active`; it does not delete memberships.
- [ ] Prepare deployment/upgrade notes, including owner password invitations
  and the requirement for working email configuration.

## Publish In The Required Order

1. Release owner pushes the protected SemVer tag on the agreed merged product
   commit using the repository's release procedure.
2. Prepare and independently merge the released changelog section, pointing to
   the tagged source. Do not rewrite older released sections.
3. Publish the GitHub release body with a resolving Full changelog link and
   deployment/upgrade instructions for the operator.
4. Fill `docs/project-plan.md#rel-09` with Released, Checked QRs, the quality
   testing-plan link and Checked UATs. A checked test need not have passed.
5. Record actual velocity from completed story points and triage unfinished
   issues. Do not count task/PR totals as points or close the sprint early.
6. When the owner authorizes the final submission, merge its report/evidence,
   verify that main commit and take the matching permalink/snapshot.

The final report, private wrapper and ZIP remain on hold until owner approval.
