import re
from typing import List
from datetime import datetime

from src.modules.listings.listings_db import ListingsDb
from src.modules.listings.listing_dataclass import Listing
from src.modules.listings.listing_purposes import ListingPurposes

DECIMAL_POINTS_REGEX = r"\.(\d+)"
COMMA_REGEX = r","
CONSECUTIVE_DIGITS_REGEX = r'\d{2,6}'
NUM_DAYS_IN_A_WEEK = 7
NUM_DAYS_IN_A_YEAR = 365
NUM_MONTHS_IN_A_YEAR = 12
DATE_ONLY_FORMAT = r"%Y-%m-%d"
MOVE_IN_DATE_ORIGINAL_FORMAT = r"%d/%m/%y"
DATETIME_FORMAT = r"%Y-%m-%d %H:%M:%S"


class ListingTransformer:
    def __init__(self, db: ListingsDb):
        self.db = db

    def remove_leading_zeroes(self, price: str):
        """Remove leading zeroes if any

        Args:
            price (str): e.g "0123" or "1000"
        """
        price.lstrip("0")

    def round_to_nearest_integer(self, price: str):
        """Round to whole number for easier display

        Args:
            price (str): e.g "3.50" or "1000.123"
        """
        price = str(round(float(price)))

    def get_average_price_from_range(self, lower: str, upper: str) -> str:
        """If a range of prices is provided, get the midpoint

        Args:
            lower (str): lower limit of the range
            upper (str): upper limit of the range

        Returns:
            str: average price
        """
        avg = (float(lower) + float(upper))/2
        return str(int(avg))

    def remove_price_formatting(self, price: str) -> str:
        r"""Remove commmon price formatting like "," (e.g 100,000) and 
        ".\d+" (e.g .00 .123)

        Args:
            price (str): e.g 100,000, 123.00

        Returns:
            str: e.g 100000, 123
        """
        #
        price_without_formats = re.sub(DECIMAL_POINTS_REGEX, "", price)
        price_without_formats = re.sub(
            COMMA_REGEX, "", price_without_formats)
        return price_without_formats

    def calculate_price_per_week(self, prices: List[str]) -> str:
        """Assume prices provided are either as a single number or a range (with
        lower and upper bounds only)
        - If single number, return that price
        - If range, get average of lower and upper limits
        - Otherwise return None price

        Args:
            prices (List[str]): e.g ["1000"], ["450", "500"]

        Returns:
            str: e.g 1000, 475
        """
        if len(prices) == 1:
            return prices[0]
        elif len(prices) == 2:
            return self.get_average_price_from_range(
                lower=prices[0], upper=prices[1])
        else:
            return None

    def set_price_per_week(self, listing: Listing, price: str):
        r"""Cleaning work for raw price data, assume all price listed are per week
        - Remove "," and ".\d+" patterns
        - Find groups of consecutive digits, min 2 and max 6 digits in a group
        - If 1 group found, that's the price
        - If 2 groups found, that's a range, calculate avg
        - Anything else results in a None price

        Args:
            listing (Listing): listing to be insterted to DB
            price (str): raw data for price
        """
        # Find digit groups with at least 2 digits next to each other, and maximum 2 groups should be found only
        # 1 group should not be more than 6 digits (i.e $100000), and min 2 digits
        # https://stackoverflow.com/questions/30776617/limit-the-number-of-digits-in-regex
        groups_of_digits = re.findall(
            CONSECUTIVE_DIGITS_REGEX, self.remove_price_formatting(price))

        price_per_week = self.calculate_price_per_week(groups_of_digits)

        if price_per_week:
            self.remove_leading_zeroes(price_per_week)
            self.round_to_nearest_integer(price_per_week)

        listing.price_per_week = price_per_week

    def set_price_per_month(self, listing: Listing):
        """Based on price per week, calculate price per month using formula from
        https://www.micm.com.au/p/how-does-monthly-rent-calculation-work/

        Args:
            listing (Listing): listing to be insterted to DB
        """
        if listing.price_per_week:
            price_per_day = int(listing.price_per_week)/NUM_DAYS_IN_A_WEEK
            price_per_year = price_per_day * NUM_DAYS_IN_A_YEAR
            price_per_month = price_per_year/NUM_MONTHS_IN_A_YEAR
            listing.price_per_month = str(round(price_per_month))
        else:
            listing.price_per_month = None

    def parse_datetime_to_date(self,
                               datetime_data: str,
                               original_format: str = DATETIME_FORMAT) -> str:
        """Parse datetime to date only format

        Args:
            datetime_data (str): date and time string

        Returns:
            str: date only
        """
        date = datetime.strptime(datetime_data, original_format)
        return date.strftime(DATE_ONLY_FORMAT)

    def set_move_in_date(self, listing: Listing, move_in_date: str):
        """Convert move in date format to standard one
        Edge case: move in date can be "NOW", convert that to posted_date in
        our standard format

        Args:
            listing (Listing): listing to be insterted to DB
            move_in_date (str): e.g 01/01/22 or NOW
        """
        try:
            datetime.strptime(move_in_date, MOVE_IN_DATE_ORIGINAL_FORMAT)
            date = self.parse_datetime_to_date(
                move_in_date, MOVE_IN_DATE_ORIGINAL_FORMAT)
            listing.move_in_date = date
        except ValueError as e:
            print(
                f"Incorrect move_in_date format: {move_in_date}, should be {MOVE_IN_DATE_ORIGINAL_FORMAT}")
            # Assume that posted_date has been processed already, not the best, but it'll do for now
            listing.move_in_date = listing.posted_date

    def get_or_create_listing_id(self,
                                 property_id: int,
                                 agent_id: int,
                                 id_from_raw: int,
                                 price: str,
                                 move_in_date: str,
                                 property_url: str,
                                 ad_posted_date: str,
                                 ad_removed_date: str,
                                 listing_title: str,
                                 listing_description: str,
                                 property_images: List[str]) -> int:
        listing = Listing()
        listing.property_id = property_id
        listing.agent_id = agent_id
        listing.id_from_raw = id_from_raw
        listing.listing_url = property_url
        listing.posted_date = self.parse_datetime_to_date(str(ad_posted_date))
        listing.removed_date = self.parse_datetime_to_date(
            str(ad_removed_date))
        listing.listing_title = listing_title
        listing.listing_description = listing_description
        listing.images = property_images
        listing.listing_purpose = ListingPurposes.rent.name

        self.set_price_per_week(listing, price)
        self.set_price_per_month(listing)

        # call this after listing.posted_date is populated
        self.set_move_in_date(listing, str(move_in_date))

        row = self.db.select_one(
            property_id=listing.property_id,
            agent_id=listing.agent_id,
            id_from_raw=listing.id_from_raw,
            posted_date=listing.posted_date,
            removed_date=listing.removed_date)
        if row:
            print("Listing data already existed")
            return {**row}['id']
        else:
            print("Listing data not collected, inserting...")
            new_id = self.db.insert_one(vars(listing))
            return {**new_id}['id']
