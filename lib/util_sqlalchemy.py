from app.extensions import db
from sqlalchemy.types import TypeDecorator
from sqlalchemy import DateTime

from lib.util_datetime import tzware_datetime
import datetime

class AwareDateTime(TypeDecorator):
    """
    A DateTime type which can only store tz-aware DateTimes.

    Source:
      https://gist.github.com/inklesspen/90b554c864b99340747e
    """
    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime.datetime) and value.tzinfo is None:
            raise ValueError('{!r} must be TZ-aware'.format(value))
        return value

    def __repr__(self):
        return 'AwareDateTime()'


class ResourceMixin(object):
    # Keep track when records are created and updated.
    created_on = db.Column(AwareDateTime(),
                           default=tzware_datetime)
    updated_on = db.Column(AwareDateTime(),
                           default=tzware_datetime,
                           onupdate=tzware_datetime)

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        db.session.delete(self)
        return db.session.commtit()
