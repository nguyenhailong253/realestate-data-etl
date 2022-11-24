import pytest
from unittest.mock import MagicMock

from src.modules.listings.listing_transformer import ListingTransformer, ListingsDb
from src.modules.listings.listing_dataclass import Listing


@pytest.fixture
def listing_transformer(mocker):
    mocker.patch("src.modules.listings.listings_db.ListingsDb.__init__",
                 return_value=None)
    db = ListingsDb(MagicMock(), MagicMock())
    transformer = ListingTransformer(db)
    return transformer


@pytest.mark.parametrize(
    "raw_price, price_per_week",
    [
        ("$680pw", "680"),  # typical price
        ("$2,000pw", "2000"),  # price with a comma
        ("$520 per week", "520"),  # price with "per week"
        ("$370.00 Per Week", "370"),  # price with "Per Week" and a "."
        ("NRAS $317.13 per week", "317"),  # take whole price only, no decimal
        ("$1,150", "1150"),  # price without text
        ("$550/week", "550"),  # price with "/week"
        ("FURNISHED $690P/W", "690"),  # price with "p/w"
        ("For Lease - 510 Pwk", "510"),  # price with "pwk"
        ("$530 per week Negotiable", "530"),  # price with random words
        ("$60 p.w.", "60"),  # price with "p.w."
        ("$530 Weekly", "530"),  # price with "Weekly"
        ("$440 - $450 / Wk, Avail Now", "445"),  # price with "/ Wk"
        ("$390 - $410 / Wk", "400"),  # Take the midpoint if there's a range
        ("$1,250-$1,300 per week", "1275"),  # Another price with range
        ("$870 - $900 per week", "885"),  # Another price with range
        ("Neg $650/$690pw *Furnished", "670"),  # Take midpoint
        ("Deposit Taken Inspection Cancelled", None),  # Price without numbers
        # Price with other numbers, i.e 2 Bedrooms
        ("Share House - 2 Bedrooms Available $200pw", "200"),
        ("1 month to 2 month rent $1000 per week", "1000"),
        ("$425pw or $525pw", "475"),  # Take midpoint
        ("$390 to $400 Per Week", "395"),  # Take midpoint
        ("850", "850"),  # Just number
        ("780+", "780"),  # Just number with a "+"
        ("Unit $750, whole house $1400", "1075"),  # Take midpoint
        ("Tenant Secured by Kade Ashton 0450 647 015", None),  # too many numbers
        ("SPACIOUS @ $490 p/wk", "490"),  # price with "p/wk"
        ("Share House - B1 $230, B4 $210", "220"),  # Take midpoint
        # take midpoint and round to whole number
        ("Deposit Taken Raine & Horne Five Dock 8757 0888", "4822")
    ]
)
def test_set_price_per_week(listing_transformer, raw_price, price_per_week):
    listing = Listing()
    listing_transformer.set_price_per_week(listing, raw_price)

    assert listing.price_per_week == price_per_week


@pytest.mark.parametrize(
    "price_per_week, price_per_month",
    [
        ("300", "1304"),
        (None, None),
    ]
)
def test_set_price_per_month(listing_transformer, price_per_week, price_per_month):
    listing = Listing()
    listing.price_per_week = price_per_week
    listing_transformer.set_price_per_month(listing)

    assert listing.price_per_month == price_per_month


def test_parse_datetime_to_date(listing_transformer):
    date = "2022-11-07 07:06:34"
    assert listing_transformer.parse_datetime_to_date(date) == "2022-11-07"


@pytest.mark.parametrize(
    "raw_move_in_date, posted_date, formatted_move_in_date",
    [
        ("10/11/22", "2022-11-07 07:06:34", "2022-11-10"),
        ("7/11/22", "2022-11-07 07:06:34", "2022-11-07"),
        ("7/1/22", "2022-11-07 07:06:34", "2022-01-07"),
        ("07/01/22", "2022-11-07 07:06:34", "2022-01-07"),
        ("now", "2022-11-08", "2022-11-08"),
    ]
)
def test_set_move_in_date(listing_transformer, raw_move_in_date, posted_date, formatted_move_in_date):
    listing = Listing()
    listing.posted_date = posted_date
    listing_transformer.set_move_in_date(listing, raw_move_in_date)

    assert listing.move_in_date == formatted_move_in_date
