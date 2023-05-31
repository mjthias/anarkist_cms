# pylint: disable=W0622,R0904,C0115,W1404
import unittest
import utils.validation as validate

##############################

class UnitTest(unittest.TestCase):

    # UTILS.VALIDATION

    ##############################

    # ID
    def test_valid_ids(self):
        cases = [
            ("1", 1),
            (1, 1),
            ("999999999", 999999999),
            (999999999, 999999999),
            ("18446744073709551615", 18446744073709551615),
            (18446744073709551615,18446744073709551615),
        ]
        for input, expected_value in cases:
            value, error = validate.id(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_ids(self):
        cases = ["", "-10", -10, "0", 0, "18446744073709551616", 18446744073709551616]
        for input in cases:
            value, error = validate.id(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # LIMIT
    def test_valid_limits(self):
        cases = [
            ("", 50),
            ("-1", -1),
            (-1, -1),
            ("1", 1),
            (1, 1),
            ("50", 50),
            (50, 50),
            ("999999999", 999999999),
            (999999999, 999999999),
        ]
        for input, expected_value in cases:
            value, error = validate.limit(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_limits(self):
        cases = [-2, "-2", "0", 0]
        for input in cases:
            value, error = validate.limit(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # OFFSET
    def test_valid_offsets(self):
        cases = [
            ("", 0),
            ("0", 0),
            (0, 0),
            ("50", 50),
            (50, 50),
            ("999999999", 999999999),
            (999999999, 999999999),
        ]
        for input, expected_value in cases:
            value, error = validate.offset(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_offsets(self):
        cases = [-1, "-1"]
        for input in cases:
            value, error = validate.offset(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # EMAIL
    def test_valid_emails(self):
        cases = [
            ("mail@mail.com", "mail@mail.com"),
            ("mail@mail.dk", "mail@mail.dk"),
            (" mail@mail.com ", "mail@mail.com"),
            ("maiL@MAIL.com", "mail@mail.com"),
            ("a@a.com", "a@a.com"),
        ]
        for input, expected_value in cases:
            value, error = validate.email(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_email(self):
        cases = ["", "mailmail.com", "mail@mailcom", "mail@mail.", "mail@mail.d", "mail@mail.ddkk", "a@.com", "@a.com"]
        for input in cases:
            value, error = validate.email(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # PASSWORD
    def test_valid_passwords(self):
        cases = [
            ("ASDddd1!", "ASDddd1!"),
            ("ASDasd123!", "ASDasd123!"),
            ("SDJKkjs12?#@-%&!", "SDJKkjs12?#@-%&!"),
            ("SDJKkjs12?#@-%&!", "SDJKkjs12?#@-%&!"),
        ]
        for input, expected_value in cases:
            value, error = validate.password(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_passwords(self):
        cases = ["", "ASDd1!", "asdasd1!", "ASDASD1!", "ASDasd123", "ASDasd!!!!"]
        for input in cases:
            value, error = validate.password(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # PASSWORD
    def test_valid_confirm_passwords(self):
        cases = [
            ("ASDasd123!", "ASDasd123!")
        ]
        for input, expected_value in cases:
            value, error = validate.confirm_password(input, "ASDasd123!")
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_confirm_passwords(self):
        cases = ["", " ASDasd123! ", "ASDasd123!!"]
        for input in cases:
            value, error = validate.confirm_password(input, "ASDasd123!")
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # USER NAME
    def test_valid_user_names(self):
        cases = [
            ("Hector Sausage-Hausen", "Hector Sausage-Hausen"),
            ("Mathias d'Arras", "Mathias d'Arras"),
            ("Bo", "Bo"),
            ("Jørgen Åge Ælbek", "Jørgen Åge Ælbek"),
            ("Jørgen de Ælbek", "Jørgen de Ælbek"),
        ]
        for input, expected_value in cases:
            value, error = validate.user_name(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_user_names(self):
        cases = ["", "A", 123, "jørgen de ælbek"]
        for input in cases:
            value, error = validate.user_name(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # BREWERY NAME
    def test_valid_brewery_names(self):
        cases = [
            ("Anarkist", "Anarkist"),
            (" Anarkist ", "Anarkist"),
            ("123-Brewery", "123-Brewery"),
            ("ÅBEN", "ÅBEN"),
            ("anarkist", "anarkist"),
            ("TOO OLD TO DIE YOUNG", "TOO OLD TO DIE YOUNG"),
        ]
        for input, expected_value in cases:
            value, error = validate.brewery_name(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_brewery_names(self):
        cases = ["", "A", "#%!"]
        for input in cases:
            value, error = validate.brewery_name(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # BREWERY MENU NAME
    def test_valid_brewery_menu_names(self):
        cases = [
            ("Anarkist", "", "Anarkist"),
            ("Anarkist", " Anarkist " ,"Anarkist"),
            ("123-Brewery", "", "123-Brewery"),
            ("ÅBEN", "ÅBEN" ,"ÅBEN"),
            ("anarkist", "anarkist","anarkist"),
            ("TOO OLD TO DIE YOUNG", "", "TOO OLD TO DIE YOUNG"),
            ("Too Old To Die Young", "TOTDY", "TOTDY")
        ]
        for input1, input2, expected_value in cases:
            value, error = validate.brewery_menu_name(input1, input2)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_brewery_menu_names(self):
        cases = [
            ("a"*101, "", None),
            ("A"*101, "A"*51, None),
            ("#%!", "#%!", None)
        ]
        for input1, input2, expected_result in cases:
            value, error = validate.brewery_menu_name(input1, input2)
            self.assertEqual(value, expected_result)
            self.assertEqual(type(error), str)

    ##############################

    # CONFIRM DELETION
    def test_valid_confirm_deletion(self):
        cases = [
            ("DELETE", "DELETE"),
        ]
        for input, expected_value in cases:
            value, error = validate.confirm_deletion(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_confirm_deletion(self):
        cases = ["", "DELTEE", "DEL", "DELETE ", "DELETEE" "delete"]
        for input in cases:
            value, error = validate.confirm_deletion(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # NAME
    def test_valid_name(self):
        cases = [
            ("Test", "Test"),
            ("TEST", "TEST"),
            (" TEST ", "TEST"),
            ("ØL2", "ØL2"),
            ("#€%", "#€%"),
        ]
        for input, expected_value in cases:
            value, error = validate.name(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_name(self):
        cases = ["", "A"]
        for input in cases:
            value, error = validate.name(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # ZIP CODE
    def test_valid_zip_code(self):
        cases = [
            ("1000", "1000"),
            ("5000", "5000"),
            ("9990", "9990"),
        ]
        for input, expected_value in cases:
            value, error = validate.zip_code(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_zip_code(self):
        cases = ["", "999", "9991", "asdd"]
        for input in cases:
            value, error = validate.zip_code(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # EBC
    def test_valid_ebc(self):
        cases = [
            ("", ""),
            ("1", "1"),
            ("500", "500"),
            ("100", "100"),

        ]
        for input, expected_value in cases:
            value, error = validate.ebc(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_ebc(self):
        cases = ["a", "601", "0"]
        for input in cases:
            value, error = validate.ebc(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # IBU
    def test_valid_ibu(self):
        cases = [
            ("", ""),
            ("1", "1"),
            ("500", "500"),
            ("100", "100"),

        ]
        for input, expected_value in cases:
            value, error = validate.ibu(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_ibu(self):
        cases = ["a", "601", "0"]
        for input in cases:
            value, error = validate.ibu(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # PRICE
    def test_valid_prices(self):
        cases = [
            ("0", 0.0),
            ("55", 55.0),
            ("55.5", 55.5),
            ("55.56", 55.56),
        ]
        for input, expected_value in cases:
            value, error = validate.price(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_prices(self):
        cases = ["a", -1, "-1"]
        for input in cases:
            value, error = validate.price(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # DESCRIPTIONS
    def test_valid_descriptions(self):
        cases = [
            ("", ""),
            (" This is a re4lly nice b33r #!%", " This is a re4lly nice b33r #!%"),
        ]
        for input, expected_value in cases:
            value, error = validate.description(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_descriptions(self):
        cases = ["a"*501]
        for input in cases:
            value, error = validate.description(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)

    ##############################

    # ROLE ID
    def test_valid_role_ids(self):
        cases = [
            ("1", 1),
            ("2", 2),
            ("3", 3),
        ]
        for input, expected_value in cases:
            value, error = validate.role_id(input)
            self.assertEqual(value, expected_value)
            self.assertEqual(error, None)

    def test_invalid_role_ids(self):
        cases = ["a", "0", "4", "-1"]
        for input in cases:
            value, error = validate.role_id(input)
            self.assertEqual(value, None)
            self.assertEqual(type(error), str)


# Only run test if file is executed
if __name__ == '__main__':
    unittest.main()
