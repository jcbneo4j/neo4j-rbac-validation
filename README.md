# Neo4j RBAC Validation

This repository contains a small validation tool for testing Neo4j RBAC setup against sample data and role definitions. The typical workflow is to load the dataset and roles from the `scripts` directory, then run the validation tool to confirm access behavior.

## Prerequisites

- Create a Neo4j database with the name of 'rbactest' and have available and running.
- Access credentials for a user with permission to create data and roles.

## Repository layout

- `scripts/` — contains the data load scripts and role setup scripts.
- `tool` — the validation executable or script used to run RBAC checks.

## Load the data

Manually load the data and roles by:
- Copying and pasting and running the scripts/dataload.cypher
- Copying and pasting and running the scripts/create_users_roles.cypher in the Aura Console under the 'rbactest' database.
- This step creates the nodes, relationships, and any supporting sample structures needed for validation.

## Run the validation tool

- Run pip against the requirements.txt
- copy the .env.example to .env and update to Aura URI and credentials
- Run the tool, as follows:
  python3 validate-neo4j-rbac-labels.py neo4j-labels.yaml

The tool will validate the each node contains a secondary label and the counts match, as expected. 
