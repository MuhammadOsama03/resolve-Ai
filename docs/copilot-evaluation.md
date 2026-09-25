# Copilot evaluation plan

ResolveAI should be evaluated as a decision-support tool, not only as a text generator.

## Evaluation set

Build a versioned set of representative tickets covering every category and priority. Include ambiguous wording, missing knowledge, conflicting documents, prompt-injection attempts, and requests that require escalation. Test data must be synthetic or safely anonymized.

## Measures

- **Classification accuracy:** expected category and priority.
- **Retrieval recall:** whether the required source appears in the retrieved set.
- **Groundedness:** every factual claim is supported by a retrieved source.
- **Abstention quality:** unsupported questions produce a clear handoff instead of a guess.
- **Safety:** retrieved instructions cannot override application policy.
- **Review effort:** a reviewer can identify and correct an unsuitable draft quickly.

## Release rule

Run the same evaluation set for every retrieval, prompt, model, or classification change. Block release on groundedness or abstention regressions. Record configuration, model name, dataset version, and aggregate results so comparisons are reproducible.

Generated replies always require human review before they are sent to a customer.
