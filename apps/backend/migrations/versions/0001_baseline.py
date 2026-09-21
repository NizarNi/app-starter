"""Establish migration history without creating domain tables."""

revision = "0001_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """The project foundation has no domain schema yet."""


def downgrade() -> None:
    """No domain schema was created by this baseline."""
