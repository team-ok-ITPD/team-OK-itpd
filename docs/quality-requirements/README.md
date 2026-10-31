# Quality requirements

This index is the priority matrix of the quality requirements. Each row finds the requirement file under `qr/`, and the scenario lives in that file.

| QR                   | Outcome                                                                                                                              | Business importance | Technical risk | Characteristic         | Sub-characteristic | Status |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------- | -------------- | ---------------------- | ------------------ | ------ |
| [QR-01](qr/QR-01.md) | Each exercise contains the bug it promises, and its tests fail on the buggy program and pass on the correct one.                     | High                | High           | Functional Suitability | Functional Correctness | Active |
| [QR-02](qr/QR-02.md) | A program a learner runs cannot read another learner's files or the host's files, and one that runs away is stopped without affecting other learners. | High                | High           | Security               | Resistance         | Active |
| [QR-03](qr/QR-03.md) | A developer can run the product's checks from a clean checkout with one documented command, and a broken change to a critical module makes them fail. | High                | Medium         | Maintainability        | Testability        | Active |
| [QR-04](qr/QR-04.md) | A learner who asks for an exercise in the catalog sees the answer within two seconds and has the exercise open in the workspace within 30 seconds. | Medium              | Medium         | Performance Efficiency | Time Behaviour     | Active |
| [QR-05](qr/QR-05.md) | A learner who has changed or broken the exercise can restore the original buggy version within two minutes, and it fails the same tests as before. | Medium              | Low            | Reliability            | Recoverability     | Active |

Active means a requirement the product is expected to meet, not a passed test or Customer acceptance. The numerical targets remain proposals for Customer review. The current deployment is learner-local; the shared-service scenario is a future target, not an implemented hosting model. Dedicated quality-test evidence is not asserted by this index.

The tests and their results are in [the testing plan](../project-plan.md#quality-requirement-testing-plan).
