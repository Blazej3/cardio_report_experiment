# Cardio Report Generator - Thesis Experimental Prototype

This repository contains two versions of the **Cardio Report Generator**, a lightweight Python-based project developed in two versions for experimental testing  the bachelor's thesis:

> **"Adapting Coding and QA Practices for Using AI-Assisted Coding Tools in the European Regulated Healthcare Environments"**

The project is non-medical, research-only, and designed to evaluate software quality, maintainability, and reproducibility between AI-assisted and manual coding workflows.

The Cardio Report Generator simulates a simplified cardiovascular reporting pipeline:
1. Accepts mock patient JSON input (see example below).
2. Generates synthetic test data (e.g., velocity, IMT, ratio values).
3. Produces a descriptive (not diagnostic) summary.
4. Renders results as an HTML report.
5. Converts the HTML into a PDF report.
6. Includes unit tests and code quality checks for reproducibility.

## Experiment Context

- Objective: Compare AI-assisted coding vs manual coding in terms of code quality, test coverage, and development efficiency.
- Scope: Non-diagnostic prototype for controlled evaluation only.
- Dataset: Generated mock JSON data (synthetic, no personal or real patient information).