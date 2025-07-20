# FollowUp.ai

This repository hosts the source code and documentation for FollowUp.ai, a WhatsApp CRM.

To understand the system architecture and guidelines, read the [development blueprint](./blueprint.md).

## Building the documentation

The documentation lives in `docs/`. To build the HTML pages locally:

```bash
pip install sphinx
make -C docs html
```

The generated site will be in `docs/build/html`.
