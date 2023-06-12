import argparse
from typing import List

from db import db
from encryption import EncryptionManager, GpgKeyNotFoundError
from management import app_context
from models import Source


def remove_pending_sources(args: argparse.Namespace) -> int:
    """
    Removes pending source accounts, with the option of keeping
    the `args.keep_most_recent` newest source accounts.
    """
    sources = find_pending_sources(args.keep_most_recent)
    print(f"Found {len(sources)} pending sources")

    for source in sources:
        try:
            EncryptionManager.get_default().delete_source_key_pair(source.filesystem_id)
        except GpgKeyNotFoundError:
            pass
        delete_pending_source(source)

    print(f"Deleted {len(sources)} pending sources")
    return 0


def find_pending_sources(keep_most_recent: int) -> List[Source]:
    """
    Finds all sources that are marked as pending
    """
    with app_context():
        return (
            Source.query.filter_by(pending=True)
            .order_by(Source.id.desc())
            .offset(keep_most_recent)
            .all()
        )


def delete_pending_source(source: Source) -> None:
    """
    Delete a pending source from the database
    """
    if source.pending:
        with app_context():
            try:
                db.session.delete(source)
                db.session.commit()
            except Exception as exc:
                db.session.rollback()
                print(f"ERROR: Could not remove pending source: {exc}.")
