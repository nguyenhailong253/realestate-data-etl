import pytest
from unittest.mock import MagicMock

from src.modules.addresses.address_transformer import AddressTransformer, AddressesDb
from src.modules.addresses.address_dataclass import Address


@pytest.fixture
def address_transformer(mocker):
    mocker.patch("src.modules.addresses.addresses_db.AddressesDb.__init__",
                 return_value=None)
    db = AddressesDb(MagicMock(), MagicMock())
    transformer = AddressTransformer(db)
    return transformer


@pytest.mark.parametrize(
    "raw_address, unit_num, street_num, street_name, street_type, street_abbrev",
    [
        # Normal address with unit number and street number
        ("8/501-503 Blaxland Road, Denistone East",
         "8", "501-503", "Blaxland", "Road", "Rd"),

        # No unit number
        ("53a Lake Avenue, Cringila", None, "53A", "Lake", "Avenue", "Ave"),

        # Address with "Unit"
        ("Unit 18/7 Hopegood Pl, Garran", "18", "7", "Hopegood", "Place", "Pl"),

        # Address with "Berth"
        ("Berth 73/7 Arcadia Court, North Haven",
         "73", "7", "Arcadia", "Court", "Ct"),

        # Address with "CP LOT" - aka carpark lot
        ("CP LOT 30/308 Pitt Street, Sydney", "30", "308", "Pitt", "Street", "St"),

        # Address with "ID:"
        ("ID:21086503/363 Turbot Street, Spring Hill",
         "21086503", "363", "Turbot", "Street", "St"),

        # Address with "Car Space"
        ("Car Space 1193Y/11 Rose Lane, Melbourne",
         "1193Y", "11", "Rose", "Lane", "Lane"),

        # Address with "FLAT"
        ("FLAT 3/10 HODDLE STREET, ELSTERNWICK",
         "3", "10", "Hoddle", "Street", "St"),

        # Address with special unit "F5.02"
        ("F5.02/41 Flora Street, KIRRAWEE", "F5.02", "41", "Flora", "Street", "St"),

        # Address with regex r'level(\d+)/'
        ("Level8/21 Cadigal Avenue, PYRMONT",
         None, "21", "Cadigal", "Avenue", "Ave"),

        # Address with regex r'level (\d+) at'
        ("LEVEL 2 at 95 Arlington Esplanade, CLIFTON BEACH",
         None, "95", "Arlington", "Esplanade", "Esp"),

        # Address with regex r'level (\d+)/'
        ("Level 10/61 Macquarie Street, Sydney",
         None, "61", "Macquarie", "Street", "St"),

        # Address with regex r'level (\d+)/'
        ("Level 1/105/566 Cotter Road, Wright",
         "105", "566", "Cotter", "Road", "Rd"),

        # Address with regex r'(\d+) bedroom/'
        ("2 Bedroom/116 Waymouth Street, Adelaide",
         None, "116", "Waymouth", "Street", "St"),

        # Address with regex r'the studio -'
        ("The Studio - 40 Asturian Drive, Henley Brook",
         None, "40", "Asturian", "Drive", "Dr"),

        # Address with regex r'l(\d+)', r'(\d+)bed/'
        ("L9 3Bed/71 Doggett Street, NEWSTEAD",
         None, "71", "Doggett", "Street", "St"),

        # Address with "Shop"
        ("Shop 2/37 Champ Elysees Esplanade, CORONET BAY",
         "2", "37", "Champ Elysees", "Esplanade", "Esp"),

        # Address with "."
        ("8. Ozone Street, CRONULLA",
         None, "8.", "Ozone", "Street", "St"),

        # Address with "Room"
        ("Room 4/1 McIntosh Crescent, Armidale",
         "4", "1", "Mcintosh", "Crescent", "Cres"),

        # Address with "... bedroom"
        ("Three Bedroom/141 Campbell Street, Bowen Hills",
         None, "141", "Campbell", "Street", "St"),

        # Address with mispelled street type
        ("3B Woodfield Boulevarde, CARINGBAH", None,
         "3B", "Woodfield", "Boulevard", "Bvd"),

        # Address where road name has direction (N, S, E, W), should ignore the direction
        ("5/1 Goodrich Road West, MURRUMBA DOWNS",
         "5", "1", "Goodrich", "Road", "Rd"),
        ("ID:21089325/165 Ekibin Road East, Tarragindi",
         "21089325", "165", "Ekibin", "Road", "Rd"),
        ("58 Grace Street South", None, "58", "Grace", "Street", "St"),
        ("1/28 Belmont Avenue Nth, Glen Iris",
         "1", "28", "Belmont", "Avenue", "Ave"),

        # Address where street type has non-alphanumeric characters
        ("12 Denman Drive., Point Cook", None, "12", "Denman", "Drive", "Dr"),
        ("9 Gregory Street., VICTORY HEIGHTS",
         None, "9", "Gregory", "Street", "St"),
        (" 43/2A Tangarra St East., Croydon Park",
         "43", "2A", "Tangarra", "Street", "St")
    ]
)
def test_normalise_street_data(address_transformer, raw_address, unit_num, street_num, street_name, street_type, street_abbrev):
    address = Address()
    address.display_address = raw_address
    address_transformer.normalise_street_data(address)

    assert address.unit_number == unit_num
    assert address.street_number == street_num
    assert address.street_name == street_name
    assert address.street_type == street_type
    assert address.street_type_abbrev == street_abbrev


@pytest.mark.parametrize(
    "raw_address",
    [
        ("XX Richardson Street West, Lane Cove"),
        ("LOCKLEYS"),
        ("PERTH"),
    ]
)
def test_normalise_street_data_raise_exceptions(address_transformer, raw_address):
    with pytest.raises(ValueError):
        address = Address()
        address.display_address = raw_address
        address_transformer.normalise_street_data(address)


@pytest.mark.parametrize(
    "street_type, abbrev",
    [
        ("Boulevarde", "Bvd"),
        ("Stret", "St"),
    ]
)
def test_set_street_type_success_with_minor_mispelled(address_transformer, street_type, abbrev):
    address = Address()
    address_transformer.set_street_type(address, street_type)

    assert address.street_type_abbrev == abbrev


@pytest.mark.parametrize(
    "street_type",
    [
        ("Test"),
        ("Not a type"),
    ]
)
def test_set_street_type_raise_exceptions(address_transformer, street_type):
    with pytest.raises(AttributeError):
        address = Address()
        address_transformer.set_street_type(address, street_type)


@pytest.mark.parametrize(
    "gps, latitude, longitude",
    [
        ("GPS Location: 0, 0", "0", "0"),
        ("GPS Location: -33.82081223, 151.22966003", "-33.82081223", "151.22966003"),
    ]
)
def test_set_latitude_longitude_data(address_transformer, gps, latitude, longitude):
    address = Address()
    address_transformer.set_latitude_longitude_data(gps, address)

    assert address.latitude == latitude
    assert address.longitude == longitude
