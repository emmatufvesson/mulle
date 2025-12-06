# Legacy Python Sources

This directory is a placeholder for the legacy Python source code from the `mulle/` directory.

## Purpose

During the TypeScript port, the original Python sources should be copied here for reference. This allows developers to:

1. Compare Python and TypeScript implementations side-by-side
2. Ensure behavioral parity during porting
3. Run regression tests against the original implementation

## Setup

To populate this directory, copy the Python sources:

```bash
# From the repository root
cp -r mulle/* legacy/
```

## Note

These files are for reference only and are not part of the TypeScript build. They should be excluded from TypeScript compilation (already configured in `tsconfig.json`).

The canonical Python sources remain in the `mulle/` directory.
