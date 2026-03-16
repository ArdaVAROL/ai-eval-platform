"""initial schema

Revision ID: 20260316_0001
Revises:
Create Date: 2026-03-16 20:45:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260316_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "datasets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_datasets_id"), "datasets", ["id"], unique=False)

    op.create_table(
        "prompt_versions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=False),
        sa.Column("prompt_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_prompt_versions_id"), "prompt_versions", ["id"], unique=False)

    op.create_table(
        "test_cases",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("dataset_id", sa.Integer(), nullable=False),
        sa.Column("input_text", sa.Text(), nullable=False),
        sa.Column("expected_output", sa.Text(), nullable=True),
        sa.Column("evaluation_type", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["dataset_id"], ["datasets.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_test_cases_dataset_id"), "test_cases", ["dataset_id"], unique=False)
    op.create_index(op.f("ix_test_cases_id"), "test_cases", ["id"], unique=False)

    op.create_table(
        "experiments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("dataset_id", sa.Integer(), nullable=False),
        sa.Column("prompt_version_id", sa.Integer(), nullable=False),
        sa.Column("model_name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["dataset_id"], ["datasets.id"]),
        sa.ForeignKeyConstraint(["prompt_version_id"], ["prompt_versions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_experiments_dataset_id"), "experiments", ["dataset_id"], unique=False)
    op.create_index(op.f("ix_experiments_id"), "experiments", ["id"], unique=False)
    op.create_index(op.f("ix_experiments_prompt_version_id"), "experiments", ["prompt_version_id"], unique=False)

    op.create_table(
        "experiment_runs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("experiment_id", sa.Integer(), nullable=False),
        sa.Column("test_case_id", sa.Integer(), nullable=False),
        sa.Column("output_text", sa.Text(), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=False),
        sa.Column("prompt_tokens", sa.Integer(), nullable=False),
        sa.Column("completion_tokens", sa.Integer(), nullable=False),
        sa.Column("total_tokens", sa.Integer(), nullable=False),
        sa.Column("cost_usd", sa.Float(), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["experiment_id"], ["experiments.id"]),
        sa.ForeignKeyConstraint(["test_case_id"], ["test_cases.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_experiment_runs_experiment_id"), "experiment_runs", ["experiment_id"], unique=False)
    op.create_index(op.f("ix_experiment_runs_id"), "experiment_runs", ["id"], unique=False)
    op.create_index(op.f("ix_experiment_runs_test_case_id"), "experiment_runs", ["test_case_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_experiment_runs_test_case_id"), table_name="experiment_runs")
    op.drop_index(op.f("ix_experiment_runs_id"), table_name="experiment_runs")
    op.drop_index(op.f("ix_experiment_runs_experiment_id"), table_name="experiment_runs")
    op.drop_table("experiment_runs")

    op.drop_index(op.f("ix_experiments_prompt_version_id"), table_name="experiments")
    op.drop_index(op.f("ix_experiments_id"), table_name="experiments")
    op.drop_index(op.f("ix_experiments_dataset_id"), table_name="experiments")
    op.drop_table("experiments")

    op.drop_index(op.f("ix_test_cases_id"), table_name="test_cases")
    op.drop_index(op.f("ix_test_cases_dataset_id"), table_name="test_cases")
    op.drop_table("test_cases")

    op.drop_index(op.f("ix_prompt_versions_id"), table_name="prompt_versions")
    op.drop_table("prompt_versions")

    op.drop_index(op.f("ix_datasets_id"), table_name="datasets")
    op.drop_table("datasets")
