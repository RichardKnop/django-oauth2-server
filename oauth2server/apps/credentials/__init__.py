from __future__ import absolute_import
from passlib.context import CryptContext

#
# create a single global instance for your app...
#
pwd_context = CryptContext(
    schemes=["bcrypt", ],
    default="bcrypt",

    # vary rounds parameter randomly when creating new hashes...
    all__vary_rounds = 0.1,

    # set the number of rounds that should be used...
    # (appropriate values may vary for different schemes,
    # and the amount of time you wish it to take)
    bcrypt__default_rounds = 12, # default for bcrypt
)