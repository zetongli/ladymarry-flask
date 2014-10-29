from flask import current_app

from ..core import Service
from ..utils import read_csv
from .models import Vendor


class VendorsService(Service):
    __model__ = Vendor

    def init_vendors(self, clear_exist=True):
        """This should be called only once to create Vendor objects. """
        if clear_exist:
            for vendor in self.all():
                self.delete(vendor)

        for row in read_csv(current_app.config['VENDOR_DATA_FILE']):
            for i in [1, 7, 13]:
                if not row[i]:
                    break
                vendor = self.create(
                    name=row[i],
                    location=row[i + 1],
                    price_range=row[i + 2],
                    profile_image=row[i + 3],
                    cover_image=row[i + 4],
                    website=row[i + 5])
