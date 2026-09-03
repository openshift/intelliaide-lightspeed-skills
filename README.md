# IntelliAide RCA Skills

IntelliAide is a deep troubleshooting and root-cause analysis pipeline for
OpenShift clusters. It performs a 3-pass analysis (High, Medium, Low
priority) over a must-gather archive and produces a structured diagnosis with
prioritised findings and remediation recommendations.

## How it works

1. **extract_cluster** — validates the must-gather archive mounted into the
   sandbox pod from a PVC at `/data/input`.
2. **select_files** — uses ML classification and LLM-guided file selection to
   identify the most relevant logs, events, and resource manifests.
3. **analyze_data** — chunks the selected files within the LLM context budget
   and prepares structured analysis prompts.
4. **perform_rca** — the orchestrating Claude session synthesises findings
   across all priority passes. The output schema is enforced by the Proposal
   CR's `outputSchema` field — the operator handles structured output
   compliance via the LLM API.

## Building the skills image

```bash
make build
```

Or directly:

```bash
make build CONTAINER_ENGINE=podman
```

## Image layout

The `Containerfile` copies `intelliaide/` into `/skills/intelliaide/` inside
the image. The operator mounts skill images as Kubernetes image volumes and
the agent reads `SKILL.md` from `/app/skills/intelliaide/SKILL.md` inside
the sandbox pod.

## Dependencies

Python dependencies are pre-installed in `intelliaide/vendor/` (Python 3.12,
x86-64) so that no `pip install` is required at image build time or at
runtime inside the restricted sandbox environment.

To regenerate `vendor/` for a new Python version:

```bash
make vendor
```

## Triggering

Create a `Proposal` CR that references this skills image:

```yaml
apiVersion: agentic.openshift.io/v1alpha1
kind: Proposal
metadata:
  name: intelliaide-rca
  namespace: openshift-lightspeed
spec:
  request: |
    Perform root cause analysis on the must-gather bundle
    mounted at /data/input.
  tools:
    skills:
      - image: <your-registry>/intelliaide-skills:latest
    dataSource:
      claimName: <pre-existing-pvc>
  analysis:
    agent: smart
    timeoutMinutes: 30
```

See the [operator examples][proposals] for more Proposal templates.

[proposals]: https://github.com/openshift/lightspeed-agentic-operator/blob/main/examples/setup/09-intelliaide-proposals.yaml

## License

Apache License 2.0 — see [LICENSE](LICENSE).
