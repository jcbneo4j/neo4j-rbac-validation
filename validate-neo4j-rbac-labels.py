from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import List

import yaml
from neo4j import GraphDatabase
from pydantic import BaseModel, Field, model_validator

from dotenv import load_dotenv

class LabelTest(BaseModel):
    primary_label: str = Field(min_length=1)
    secondary_labels: List[str] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_labels(self) -> "LabelTest":
        cleaned = [x.strip() for x in self.secondary_labels if x and x.strip()]
        if len(cleaned) != len(set(cleaned)):
            raise ValueError("secondary_labels contains duplicates")
        self.secondary_labels = cleaned
        return self


class TestConfig(BaseModel):
    tests: List[LabelTest] = Field(min_length=1)


class LabelCoverage(BaseModel):
    primary_label: str
    secondary_labels: List[str]
    base_count: int = Field(ge=0)
    matched_count: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_counts(self) -> "LabelCoverage":
        if self.base_count == 0:
            raise ValueError(f"no nodes found with label {self.primary_label}")
        if self.matched_count != self.base_count:
            raise ValueError(
                f"only {self.matched_count} of {self.base_count} "
                f"{self.primary_label} nodes have one of {self.secondary_labels}"
            )
        return self


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that nodes have one of the configured secondary labels."
    )
    parser.add_argument(
        "labels_file",
        help="Path to labels.yml",
    )
    return parser.parse_args()


def load_config(path: str | Path) -> TestConfig:
    data = yaml.safe_load(Path(path).read_text())
    return TestConfig.model_validate(data)


def count_coverage(driver, test: LabelTest) -> LabelCoverage:
    '''
    label_checks = " OR ".join(f"n:{label}" for label in test.secondary_labels)
    cypher = f"""
    MATCH (n:{test.primary_label})
    RETURN
      count(n) AS baseCount,
      count(CASE WHEN {label_checks} THEN 1 END) AS matchedCount
    """
    '''
    secondary_predicate = " OR ".join(f"n:{label}" for label in test.secondary_labels)
    cypher = f"""
    RETURN
      COUNT {{ MATCH (n:{test.primary_label}) RETURN n }} AS baseCount,
      COUNT {{
        MATCH (n:{test.primary_label})
        WHERE {secondary_predicate}
        RETURN n
      }} AS matchedCount
    """

    print(cypher)

    with driver.session(database=os.getenv('NEO4J_DATABASE')) as session:
        record = session.run(cypher).single()
        return LabelCoverage(
            primary_label=test.primary_label,
            secondary_labels=test.secondary_labels,
            base_count=record["baseCount"],
            matched_count=record["matchedCount"],
        )


def main() -> int:
    args = parse_args()
    config = load_config(args.labels_file)

    load_dotenv()

    driver = GraphDatabase.driver(
        os.getenv('NEO4J_URI'),
        auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')),
    )

    try:
        for test in config.tests:
            result = count_coverage(driver, test)
            print(
                f"PASS: {result.matched_count}/{result.base_count} "
                f"{result.primary_label} nodes have one of {result.secondary_labels}"
            )
        return 0
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1
    finally:
        driver.close()


if __name__ == "__main__":
    raise SystemExit(main())
