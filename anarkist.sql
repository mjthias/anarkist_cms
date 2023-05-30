-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: May 30, 2023 at 07:02 AM
-- Server version: 5.7.39
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `anarkist`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`anarkist`@`%` PROCEDURE `delete_tap` (IN `_tap_id` BIGINT UNSIGNED, IN `_bar_id` BIGINT UNSIGNED)   BEGIN
    DECLARE _max_tap_number BIGINT UNSIGNED;
    DECLARE _tap_number BIGINT UNSIGNED;
    
    SELECT MAX(tap_number) INTO _max_tap_number
    FROM taps
    WHERE fk_bar_id = _bar_id;
    
    SELECT tap_number INTO _tap_number
    FROM taps
    WHERE tap_id = _tap_id AND fk_bar_id = _bar_id;
    
    DELETE FROM taps
    WHERE tap_id = _tap_id AND fk_bar_id = _bar_id;

    IF _tap_number IS NOT NULL 
    AND _tap_number != _max_tap_number 
    THEN
        UPDATE taps
        SET tap_number = tap_number - 1
        WHERE tap_number > _tap_number AND fk_bar_id = _bar_id;
    END IF;
    SELECT _max_tap_number;
END$$

CREATE DEFINER=`anarkist`@`%` PROCEDURE `get_beers_by_fuzzy_name` (IN `_beer_name` VARCHAR(50), IN `_limit` INT UNSIGNED, IN `_offset` INT UNSIGNED)   SELECT * FROM beers_list
WHERE LOWER(SOUNDEX(beer_name))
LIKE LOWER(REPLACE(CONCAT("%", SOUNDEX(_beer_name), "%"), " ", "%"))

OR LOWER(beer_name)
LIKE LOWER(REPLACE(CONCAT("%", (_beer_name), "%"), " ", "%"))

LIMIT _offset,_limit$$

CREATE DEFINER=`anarkist`@`%` PROCEDURE `get_beer_style_by_fuzzy_name` (IN `_beer_style_name` VARCHAR(50), IN `_offset` INT UNSIGNED, IN `_limit` INT)   SELECT * FROM beer_styles
WHERE LOWER(SOUNDEX(beer_style_name))
LIKE LOWER(REPLACE(CONCAT("%", SOUNDEX(_beer_style_name), "%"), " ", "%"))
OR LOWER(beer_style_name)
LIKE LOWER(REPLACE(CONCAT("%", (_beer_style_name), "%"), " ", "%"))
LIMIT _offset,_limit$$

CREATE DEFINER=`anarkist`@`%` PROCEDURE `get_brewery_by_fuzzy_name` (IN `_brewery_name` VARCHAR(50), IN `_offset` BIGINT UNSIGNED, IN `_limit` BIGINT UNSIGNED)   SELECT * FROM breweries
WHERE LOWER(SOUNDEX(brewery_name))
LIKE LOWER(REPLACE(CONCAT("%", SOUNDEX(_brewery_name), "%"), " ", "%"))

OR LOWER(SOUNDEX(brewery_menu_name))
LIKE LOWER(REPLACE(CONCAT("%", SOUNDEX(_brewery_name), "%"), " ", "%"))

OR LOWER(brewery_name)
LIKE LOWER(REPLACE(CONCAT("%", (_brewery_name), "%"), " ", "%"))

OR LOWER(brewery_menu_name)
LIKE LOWER(REPLACE(CONCAT("%", (_brewery_name), "%"), " ", "%"))


LIMIT _offset,_limit$$

CREATE DEFINER=`anarkist`@`%` PROCEDURE `get_users_by_fuzzy_name` (IN `_search_term` VARCHAR(100), IN `_offset` BIGINT UNSIGNED, IN `_limit` BIGINT UNSIGNED, IN `_role_id` TINYINT(3) UNSIGNED, IN `_user_id` BIGINT UNSIGNED)   SELECT * FROM users_list
WHERE LOWER(SOUNDEX(user_name))
LIKE LOWER(REPLACE(CONCAT("%", SOUNDEX(_search_term), "%"), " ", "%"))
AND user_role_id >= _role_id AND user_id != _user_id

OR LOWER(SOUNDEX(user_email))
LIKE LOWER(REPLACE(CONCAT("%", SOUNDEX(_search_term), "%"), " ", "%"))
AND user_role_id >= _role_id AND user_id != _user_id

OR LOWER(user_name)
LIKE LOWER(REPLACE(CONCAT("%", (_search_term), "%"), " ", "%"))
AND user_role_id >= _role_id AND user_id != _user_id

OR LOWER(user_email)
LIKE LOWER(REPLACE(CONCAT("%", (_search_term), "%"), " ", "%"))
AND user_role_id >= _role_id AND user_id != _user_id

LIMIT _offset,_limit$$

CREATE DEFINER=`anarkist`@`%` PROCEDURE `insert_tap` (IN `_is_off_wall` BOOLEAN, IN `_beer_id` BIGINT UNSIGNED, IN `_bar_id` BIGINT UNSIGNED)   BEGIN
    DECLARE _tap_number INT UNSIGNED;
	IF NOT _is_off_wall THEN

        SELECT COALESCE(MAX(tap_number), 0) + 1 INTO _tap_number FROM taps
        WHERE fk_bar_id = _bar_id
        LIMIT 1;

		INSERT INTO taps
        (tap_number, fk_beer_id, fk_bar_id, tap_unavailable)
        VALUES (_tap_number, _beer_id, _bar_id, 0);
        
    ELSE
    	INSERT INTO taps
        (fk_beer_id, fk_bar_id, tap_unavailable)
        VALUES (_beer_id, _bar_id, 0);
	END IF;
    SELECT LAST_INSERT_ID() as tap_id;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `bars`
--

CREATE TABLE `bars` (
  `bar_id` bigint(20) UNSIGNED NOT NULL,
  `bar_name` varchar(100) NOT NULL,
  `bar_street` varchar(100) NOT NULL,
  `bar_zip_code` char(4) NOT NULL,
  `bar_city` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bars`
--

INSERT INTO `bars` (`bar_id`, `bar_name`, `bar_street`, `bar_zip_code`, `bar_city`) VALUES
(1, 'Anarkist Bars', 'Bernstorffsgade 7', '1786', 'København V'),
(2, 'Anarkist Beer & Food Lab', 'Albanigade 20', '5000', 'Odense C');

-- --------------------------------------------------------

--
-- Table structure for table `bar_access`
--

CREATE TABLE `bar_access` (
  `fk_bar_id` bigint(20) UNSIGNED NOT NULL,
  `fk_user_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bar_access`
--

INSERT INTO `bar_access` (`fk_bar_id`, `fk_user_id`) VALUES
(1, 23),
(1, 24);

-- --------------------------------------------------------

--
-- Table structure for table `beers`
--

CREATE TABLE `beers` (
  `beer_id` bigint(20) UNSIGNED NOT NULL,
  `beer_name` varchar(50) NOT NULL,
  `fk_brewery_id` bigint(20) UNSIGNED NOT NULL,
  `beer_ebc` varchar(3) DEFAULT NULL,
  `beer_ibu` varchar(3) DEFAULT NULL,
  `beer_alc` varchar(5) NOT NULL,
  `fk_beer_style_id` bigint(20) UNSIGNED NOT NULL,
  `beer_price` double UNSIGNED NOT NULL,
  `beer_image` varchar(41) DEFAULT NULL,
  `beer_description_en` varchar(500) DEFAULT NULL,
  `beer_description_dk` varchar(500) DEFAULT NULL,
  `beer_created_at` int(10) UNSIGNED NOT NULL,
  `fk_beer_created_by` bigint(20) UNSIGNED DEFAULT NULL,
  `beer_updated_at` int(10) UNSIGNED NOT NULL,
  `fk_beer_updated_by` bigint(20) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `beers`
--

INSERT INTO `beers` (`beer_id`, `beer_name`, `fk_brewery_id`, `beer_ebc`, `beer_ibu`, `beer_alc`, `fk_beer_style_id`, `beer_price`, `beer_image`, `beer_description_en`, `beer_description_dk`, `beer_created_at`, `fk_beer_created_by`, `beer_updated_at`, `fk_beer_updated_by`) VALUES
(123, 'Fizzy Lime Fusion', 59, '12', '15', '5.00', 75, 55, 'd2db70d4-4adb-4109-aeac-436bd4661aaf.jpeg', 'Sweetness and acidity in perfect balance with a clear taste of lychee and lime, but without losing the character of beer. Full-bodied, mouth-watering and refreshingly acidic with a light finishing bitterness.', 'Sødme og syre i perfekt balance med klar smag af lychee og lime, dog uden at miste karatér af øl. Fyldig, læskende og forfriskende syrlig med en let afsluttende bitterhed.', 1685380959, 22, 1685381409, 22),
(124, 'Mighty Mild Ale', 59, '30', '30', '0.50', 138, 55, '47982e34-3ef6-475e-93cc-ca96a2f6c810.jpeg', 'A malt-driven beer with notes of grain, caramel, toast and fruitiness from the rye. A beer with a full body, a hint of sweetness and mild carbonation.', 'En maltdrevet øl med noter af korn, karamel, ristet brød og frugtighed fra rugen. En øl med en fyldig krop, en anelse sødme og mild karbonering.', 1685381706, 22, 1685381706, 22),
(125, 'Pina Colada Milkshake IPA', 59, '12', '25', '6.70', 139, 65, '453c45e6-9b0d-45f6-9872-b4587293dfa3.jpeg', 'Explosion of vanilla and pineapple balanced with a light bitterness and high sweetness. A full-bodied, mouth-watering, satiating and lush beer.', 'Eksplosion af vanilje og ananas balanceret med en let bitterhed og høj sødme. En fyldig, læskende, mættende og frodig øl.', 1685382011, 22, 1685382035, 22),
(126, 'Red Noses', 59, '35', '25', '5.50', 89, 55, '71953751-8ca5-46a6-addd-ed148e7bdbce.jpeg', 'This year we are making a Christmas beer in a more classic sense, created to match the Danish Christmas food. However, we have kept the anarchist twist. We\'ve done that by giving this rye-based Red Ale a shot of cranberry. The use of rye is as if created to accompany rye bread, and the general malt and hop composition means that this beer is going to be absolutely perfect for the Danish Christmas meal.', 'I år laver vi en juleøl i mere klassisk forstand, skabt til at passe til den danske julemad. Vi har dog bevaret det anarkistiske twist. Det har vi gjort ved at give denne rug baserede Red Ale et skud tranebær. Brugen af rug er som skabt til at ledsage rugbrød, og den generelle malt og humlesammensætning gør, at denne øl, kommer til at være helt perfekt til den danske julemad.', 1685382260, 22, 1685382260, 22),
(127, 'Expelled Club 27 Member', 60, '', '', '9.20', 76, 75, '4d1fa4e0-2475-419d-8ed4-a6fdf5ef54a3.jpeg', '', '', 1685382950, 22, 1685386403, 22),
(128, 'Heineken', 65, '', '', '5.00', 96, 50, '', '', '', 1685383170, 22, 1685383170, 22),
(129, 'Weiss Dragon', 59, '', '', '5.20', 140, 55, '15717f63-afcc-409a-a32e-c045a4b2d8a2.jpeg', '', '', 1685384007, 22, 1685384007, 22),
(130, 'Ginger Pale Ale', 59, '', '', '5.00', 107, 55, 'c634d4a7-c3d8-4f7b-af27-73b08de5847a.jpeg', '', '', 1685384120, 22, 1685384120, 22),
(131, 'Juicy Galaxy', 59, '', '', '6.40', 74, 55, 'd4a30a21-dc30-49fb-8aee-ba8144fcf049.jpeg', '', '', 1685384187, 22, 1685384187, 22),
(132, 'Organic Pilsner', 64, '', '', '4.60', 77, 50, '', '', '', 1685384704, 22, 1685384704, 22),
(133, 'Organic Classic', 64, '', '', '5.70', 96, 50, '', '', '', 1685384733, 22, 1685384733, 22),
(134, 'Resting Brew Face', 62, '', '', '7.60', 98, 65, '65489303-a8b3-48f8-ba71-69a6007c9f99.jpeg', '', '', 1685386378, 22, 1685386378, 22),
(135, 'Beer Geek Breakfast', 62, '', '', '7.50', 76, 75, 'd363e669-b81d-4f97-99ad-6d6e747eb8e3.jpeg', '', '', 1685386473, 22, 1685386986, 22),
(136, 'Revision', 60, '', '', '6.40', 82, 65, '412660ad-0c38-4356-9b2d-9a8fefe4635e.jpeg', '', '', 1685386652, 22, 1685386652, 22),
(137, 'Beer Geek Brunch', 62, '', '', '10.60', 76, 80, 'd9845512-9c03-412c-b51d-bc906dc3fd0b.jpeg', '', '', 1685386968, 22, 1685386968, 22),
(138, 'Passion Pool', 62, '', '', '6.60', 83, 70, 'b7b6acee-7c2a-4b24-86da-3dbb5a796279.jpeg', '', '', 1685387039, 22, 1685387039, 22),
(139, 'CPHaze', 61, '', '', '6.50', 75, 60, '3355a444-fe0c-494f-ae26-180fc9a974c0.jpeg', '', '', 1685387097, 22, 1685387097, 22),
(140, 'Quick n Dirty', 59, '', '', '7.40', 75, 65, 'b583b26a-58ee-4df8-8c52-1b6192ed49fd.jpeg', '', '', 1685387139, 22, 1685387284, 22),
(141, 'All My Friends Are Drunk', 60, '', '', '11.20', 105, 80, 'aa78dcea-c824-4e78-8d4b-614f32720466.jpeg', '', '', 1685387361, 22, 1685387361, 22);

-- --------------------------------------------------------

--
-- Stand-in structure for view `beers_list`
-- (See below for the actual view)
--
CREATE TABLE `beers_list` (
`beer_id` bigint(20) unsigned
,`beer_name` varchar(50)
,`fk_brewery_id` bigint(20) unsigned
,`beer_ebc` varchar(3)
,`beer_ibu` varchar(3)
,`beer_alc` varchar(5)
,`fk_beer_style_id` bigint(20) unsigned
,`beer_price` double unsigned
,`beer_image` varchar(41)
,`beer_description_en` varchar(500)
,`beer_description_dk` varchar(500)
,`beer_created_at` int(10) unsigned
,`fk_beer_created_by` bigint(20) unsigned
,`beer_updated_at` int(10) unsigned
,`fk_beer_updated_by` bigint(20) unsigned
,`brewery_name` varchar(100)
,`beer_style_name` varchar(50)
,`beer_created_by_user_name` varchar(100)
,`beer_updated_by_user_name` varchar(100)
);

-- --------------------------------------------------------

--
-- Table structure for table `beer_styles`
--

CREATE TABLE `beer_styles` (
  `beer_style_id` bigint(20) UNSIGNED NOT NULL,
  `beer_style_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `beer_styles`
--

INSERT INTO `beer_styles` (`beer_style_id`, `beer_style_name`) VALUES
(88, 'Ale'),
(130, 'Amber Ale'),
(106, 'Amercian Style Cream Ale'),
(103, 'American Amber Ale'),
(116, 'American Barley Wine'),
(134, 'American Lager'),
(99, 'American Pale Ale'),
(86, 'American Wild Ale'),
(119, 'Baltic Porter'),
(117, 'Belgian Blond Ale'),
(81, 'Berliner Weisse'),
(128, 'Bière de garde'),
(120, 'Bitter'),
(124, 'Black IPA'),
(108, 'Blonde Ale'),
(109, 'California Common'),
(125, 'Cask Ale'),
(111, 'Chocolate Beer'),
(110, 'Coffee Beer'),
(123, 'Cream Ale'),
(98, 'Dobbelbock'),
(127, 'Dortmunder Export'),
(76, 'Double IPA'),
(136, 'Dubbel'),
(104, 'English Style Brown Ale'),
(93, 'Framboise'),
(114, 'Fruit Lambic'),
(100, 'German Style Dunkel'),
(90, 'Gose'),
(118, 'Grodziskie'),
(91, 'Gueuze'),
(75, 'Hazy IPA'),
(112, 'Honey Beer'),
(137, 'Imperial Stout'),
(72, 'IPA'),
(74, 'Juicy IPA'),
(87, 'Kettle Sour'),
(95, 'Kölsch'),
(135, 'Kriek Lambic'),
(96, 'Lager'),
(94, 'Lambic'),
(126, 'Märzen'),
(138, 'Mild Ale'),
(139, 'Milkshake IPA'),
(80, 'New England IPA'),
(129, 'Oatmeal Stout'),
(107, 'Pale Ale'),
(97, 'Pale Lager'),
(77, 'Pilsner'),
(78, 'Porter'),
(115, 'Pumpkin Beer'),
(133, 'Rauchbier'),
(89, 'Red Ale'),
(92, 'Saison'),
(122, 'Schwarzbier'),
(132, 'Scotch Ale'),
(73, 'Session IPA'),
(79, 'Smoke Porter'),
(83, 'Sour'),
(82, 'Sour IPA'),
(105, 'Stout'),
(131, 'Sweet Stout'),
(140, 'Weissbier'),
(121, 'Weizenbock'),
(113, 'Witbier');

-- --------------------------------------------------------

--
-- Table structure for table `breweries`
--

CREATE TABLE `breweries` (
  `brewery_id` bigint(20) UNSIGNED NOT NULL,
  `brewery_name` varchar(100) NOT NULL,
  `brewery_menu_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `breweries`
--

INSERT INTO `breweries` (`brewery_id`, `brewery_name`, `brewery_menu_name`) VALUES
(59, 'Anarkist', 'Anarkist'),
(60, 'Too Old To Die Young', 'TOTDY'),
(61, 'To Øl', 'To Øl'),
(62, 'Mikkeller', 'Mikkeller'),
(63, 'Warpigs', 'Warpigs'),
(64, 'Royal', 'Royal'),
(65, 'Heineken', 'Heineken'),
(66, 'Aaben', 'Aaben'),
(67, 'Hancock', 'Hancock'),
(68, 'Baghaven', 'Baghaven'),
(69, 'Carlsberg', 'Carlsberg'),
(70, 'Tuborg', 'Tuborg'),
(71, 'Thisted Bryghus', 'Thisted Bryghus'),
(72, 'Kissmeyer', 'Kissmeyer'),
(73, 'Aarhus Bryghus', 'Aarhus Bryghus'),
(74, 'Ugly Duck', 'Ugly Duck'),
(75, 'Sour Feet', 'Sour Feet');

-- --------------------------------------------------------

--
-- Table structure for table `ingredients`
--

CREATE TABLE `ingredients` (
  `ingredient_id` bigint(20) UNSIGNED NOT NULL,
  `ingredient_name_en` varchar(50) NOT NULL,
  `ingredient_name_dk` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `pizzas`
--

CREATE TABLE `pizzas` (
  `pizza_id` bigint(20) UNSIGNED NOT NULL,
  `pizza_name` varchar(50) NOT NULL,
  `pizza_number` tinyint(50) NOT NULL,
  `fk_bar_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `pizza_ingredients`
--

CREATE TABLE `pizza_ingredients` (
  `fk_pizza_id` bigint(20) UNSIGNED NOT NULL,
  `fk_ingredient_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `session_id` bigint(20) UNSIGNED NOT NULL,
  `fk_user_id` bigint(20) UNSIGNED NOT NULL,
  `session_iat` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sessions`
--

INSERT INTO `sessions` (`session_id`, `fk_user_id`, `session_iat`) VALUES
(138, 22, 1685429766);

-- --------------------------------------------------------

--
-- Table structure for table `taps`
--

CREATE TABLE `taps` (
  `tap_id` bigint(20) UNSIGNED NOT NULL,
  `tap_number` tinyint(100) DEFAULT NULL,
  `fk_beer_id` bigint(20) UNSIGNED DEFAULT NULL,
  `fk_bar_id` bigint(20) UNSIGNED NOT NULL,
  `tap_unavailable` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `taps`
--

INSERT INTO `taps` (`tap_id`, `tap_number`, `fk_beer_id`, `fk_bar_id`, `tap_unavailable`) VALUES
(57, 1, 131, 1, 0),
(59, 2, 141, 1, 0),
(60, 3, 125, 1, 0),
(61, 4, 138, 1, 0),
(62, 5, 124, 1, 0),
(63, 6, 130, 1, 0),
(64, 7, 139, 1, 0),
(65, 8, 123, 1, 0),
(66, 9, 136, 1, 0),
(67, 10, 134, 1, 0),
(68, 11, 135, 1, 0),
(69, 12, 137, 1, 0),
(70, 13, 127, 1, 0),
(71, NULL, 128, 1, 0),
(72, NULL, 132, 1, 0),
(75, NULL, 133, 1, 0),
(76, 14, 140, 1, 0),
(77, 15, 126, 1, 0),
(78, 16, NULL, 1, 0),
(80, 17, 141, 1, 0);

-- --------------------------------------------------------

--
-- Stand-in structure for view `taps_list`
-- (See below for the actual view)
--
CREATE TABLE `taps_list` (
`tap_id` bigint(20) unsigned
,`tap_number` tinyint(100)
,`fk_beer_id` bigint(20) unsigned
,`fk_bar_id` bigint(20) unsigned
,`tap_unavailable` tinyint(1)
,`beer_id` bigint(20) unsigned
,`beer_name` varchar(50)
,`beer_ebc` varchar(3)
,`beer_ibu` varchar(3)
,`beer_alc` varchar(5)
,`beer_price` double unsigned
,`beer_image` varchar(41)
,`brewery_name` varchar(100)
,`beer_style_name` varchar(50)
,`beer_description_en` varchar(500)
,`beer_description_dk` varchar(500)
);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `user_password` varchar(100) NOT NULL,
  `fk_user_role_id` tinyint(3) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_email`, `user_name`, `user_password`, `fk_user_role_id`) VALUES
(22, 'super@user.dk', 'Morthias Gross Dahl', '$2b$12$mcZKnS0.O9TtbUXSQSWqv.A2EWofo3mC740IXRWRc1g3AEH3pGEGe', 1),
(23, 'bar@admin.dk', 'Mathias Gross', '$2b$12$SUwvvmTUM6mYVJTxynO6Be4JZ/Zrq5kUHYhVH2r0NoI7354u920Qa', 2),
(24, 'bar@staff.dk', 'Morten Dahl', '$2b$12$CU9IZMYR1mTkMYxb3zxOfuLOGM2xUpRnoETHmNJQl6kRtW4PG4VLW', 3);

-- --------------------------------------------------------

--
-- Stand-in structure for view `users_list`
-- (See below for the actual view)
--
CREATE TABLE `users_list` (
`user_id` bigint(20) unsigned
,`user_email` varchar(100)
,`user_name` varchar(100)
,`user_role_id` tinyint(3) unsigned
,`user_role_title` varchar(20)
,`bar_id` bigint(20) unsigned
,`bar_name` varchar(100)
,`bar_street` varchar(100)
,`bar_zip_code` char(4)
,`bar_city` varchar(100)
);

-- --------------------------------------------------------

--
-- Table structure for table `user_roles`
--

CREATE TABLE `user_roles` (
  `user_role_id` tinyint(3) UNSIGNED NOT NULL,
  `user_role_title` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_roles`
--

INSERT INTO `user_roles` (`user_role_id`, `user_role_title`) VALUES
(1, 'superuser'),
(2, 'bar admin'),
(3, 'bar staff');

-- --------------------------------------------------------

--
-- Structure for view `beers_list`
--
DROP TABLE IF EXISTS `beers_list`;

CREATE ALGORITHM=UNDEFINED DEFINER=`anarkist`@`%` SQL SECURITY DEFINER VIEW `beers_list`  AS SELECT `beers`.`beer_id` AS `beer_id`, `beers`.`beer_name` AS `beer_name`, `beers`.`fk_brewery_id` AS `fk_brewery_id`, `beers`.`beer_ebc` AS `beer_ebc`, `beers`.`beer_ibu` AS `beer_ibu`, `beers`.`beer_alc` AS `beer_alc`, `beers`.`fk_beer_style_id` AS `fk_beer_style_id`, `beers`.`beer_price` AS `beer_price`, `beers`.`beer_image` AS `beer_image`, `beers`.`beer_description_en` AS `beer_description_en`, `beers`.`beer_description_dk` AS `beer_description_dk`, `beers`.`beer_created_at` AS `beer_created_at`, `beers`.`fk_beer_created_by` AS `fk_beer_created_by`, `beers`.`beer_updated_at` AS `beer_updated_at`, `beers`.`fk_beer_updated_by` AS `fk_beer_updated_by`, `breweries`.`brewery_name` AS `brewery_name`, `beer_styles`.`beer_style_name` AS `beer_style_name`, `c`.`user_name` AS `beer_created_by_user_name`, `u`.`user_name` AS `beer_updated_by_user_name` FROM ((((`beers` join `beer_styles` on((`beers`.`fk_beer_style_id` = `beer_styles`.`beer_style_id`))) join `breweries` on((`beers`.`fk_brewery_id` = `breweries`.`brewery_id`))) left join `users` `c` on((`beers`.`fk_beer_created_by` = `c`.`user_id`))) left join `users` `u` on((`beers`.`fk_beer_updated_by` = `u`.`user_id`))) ;

-- --------------------------------------------------------

--
-- Structure for view `taps_list`
--
DROP TABLE IF EXISTS `taps_list`;

CREATE ALGORITHM=UNDEFINED DEFINER=`anarkist`@`%` SQL SECURITY DEFINER VIEW `taps_list`  AS SELECT `taps`.`tap_id` AS `tap_id`, `taps`.`tap_number` AS `tap_number`, `taps`.`fk_beer_id` AS `fk_beer_id`, `taps`.`fk_bar_id` AS `fk_bar_id`, `taps`.`tap_unavailable` AS `tap_unavailable`, `beers_list`.`beer_id` AS `beer_id`, `beers_list`.`beer_name` AS `beer_name`, `beers_list`.`beer_ebc` AS `beer_ebc`, `beers_list`.`beer_ibu` AS `beer_ibu`, `beers_list`.`beer_alc` AS `beer_alc`, `beers_list`.`beer_price` AS `beer_price`, `beers_list`.`beer_image` AS `beer_image`, `beers_list`.`brewery_name` AS `brewery_name`, `beers_list`.`beer_style_name` AS `beer_style_name`, `beers_list`.`beer_description_en` AS `beer_description_en`, `beers_list`.`beer_description_dk` AS `beer_description_dk` FROM (`taps` join `beers_list` on((`taps`.`fk_beer_id` = `beers_list`.`beer_id`))) ORDER BY (case when isnull(`taps`.`tap_number`) then 1 else 0 end) ASC, `taps`.`tap_number` ASC ;

-- --------------------------------------------------------

--
-- Structure for view `users_list`
--
DROP TABLE IF EXISTS `users_list`;

CREATE ALGORITHM=UNDEFINED DEFINER=`anarkist`@`%` SQL SECURITY DEFINER VIEW `users_list`  AS SELECT `users`.`user_id` AS `user_id`, `users`.`user_email` AS `user_email`, `users`.`user_name` AS `user_name`, `user_roles`.`user_role_id` AS `user_role_id`, `user_roles`.`user_role_title` AS `user_role_title`, `bars`.`bar_id` AS `bar_id`, `bars`.`bar_name` AS `bar_name`, `bars`.`bar_street` AS `bar_street`, `bars`.`bar_zip_code` AS `bar_zip_code`, `bars`.`bar_city` AS `bar_city` FROM (((`users` left join `user_roles` on((`users`.`fk_user_role_id` = `user_roles`.`user_role_id`))) left join `bar_access` on((`users`.`user_id` = `bar_access`.`fk_user_id`))) left join `bars` on((`bar_access`.`fk_bar_id` = `bars`.`bar_id`))) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bars`
--
ALTER TABLE `bars`
  ADD PRIMARY KEY (`bar_id`),
  ADD UNIQUE KEY `bar_name` (`bar_name`,`bar_city`);

--
-- Indexes for table `bar_access`
--
ALTER TABLE `bar_access`
  ADD PRIMARY KEY (`fk_bar_id`,`fk_user_id`),
  ADD KEY `cascade_users_on_bar_access` (`fk_user_id`);

--
-- Indexes for table `beers`
--
ALTER TABLE `beers`
  ADD PRIMARY KEY (`beer_id`),
  ADD UNIQUE KEY `beer_name` (`beer_name`,`fk_brewery_id`),
  ADD KEY `brewery_on_fk_brewery` (`fk_brewery_id`),
  ADD KEY `style_on_fk_style` (`fk_beer_style_id`),
  ADD KEY `set_null_user_on_created_by` (`fk_beer_created_by`),
  ADD KEY `set_null_user_on_updated_by` (`fk_beer_updated_by`);

--
-- Indexes for table `beer_styles`
--
ALTER TABLE `beer_styles`
  ADD PRIMARY KEY (`beer_style_id`),
  ADD UNIQUE KEY `beer_style_name` (`beer_style_name`);

--
-- Indexes for table `breweries`
--
ALTER TABLE `breweries`
  ADD PRIMARY KEY (`brewery_id`),
  ADD UNIQUE KEY `brewery_name` (`brewery_name`),
  ADD UNIQUE KEY `brewery_menu_name` (`brewery_menu_name`);

--
-- Indexes for table `ingredients`
--
ALTER TABLE `ingredients`
  ADD PRIMARY KEY (`ingredient_id`),
  ADD UNIQUE KEY `ingredient_name_en` (`ingredient_name_en`),
  ADD UNIQUE KEY `ingredient_name_dk` (`ingredient_name_dk`);

--
-- Indexes for table `pizzas`
--
ALTER TABLE `pizzas`
  ADD PRIMARY KEY (`pizza_id`),
  ADD UNIQUE KEY `pizza_number` (`pizza_number`,`fk_bar_id`),
  ADD UNIQUE KEY `pizza_name` (`pizza_name`,`fk_bar_id`),
  ADD KEY `cascade_bar_on_fk_bar` (`fk_bar_id`);

--
-- Indexes for table `pizza_ingredients`
--
ALTER TABLE `pizza_ingredients`
  ADD PRIMARY KEY (`fk_pizza_id`,`fk_ingredient_id`),
  ADD KEY `ingredient_on_fk_ingredient` (`fk_ingredient_id`);

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`session_id`),
  ADD UNIQUE KEY `fk_user_id` (`fk_user_id`),
  ADD KEY `cascade_user_on_session_user_id` (`fk_user_id`);

--
-- Indexes for table `taps`
--
ALTER TABLE `taps`
  ADD PRIMARY KEY (`tap_id`),
  ADD UNIQUE KEY `tap_number` (`tap_number`,`fk_bar_id`),
  ADD KEY `cascade_bars_on_taps` (`fk_bar_id`),
  ADD KEY `cascade_beers_on_taps` (`fk_beer_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_email` (`user_email`),
  ADD KEY `user_role_on_user` (`fk_user_role_id`);

--
-- Indexes for table `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`user_role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bars`
--
ALTER TABLE `bars`
  MODIFY `bar_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `beers`
--
ALTER TABLE `beers`
  MODIFY `beer_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=144;

--
-- AUTO_INCREMENT for table `beer_styles`
--
ALTER TABLE `beer_styles`
  MODIFY `beer_style_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=141;

--
-- AUTO_INCREMENT for table `breweries`
--
ALTER TABLE `breweries`
  MODIFY `brewery_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=78;

--
-- AUTO_INCREMENT for table `ingredients`
--
ALTER TABLE `ingredients`
  MODIFY `ingredient_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `pizzas`
--
ALTER TABLE `pizzas`
  MODIFY `pizza_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `sessions`
--
ALTER TABLE `sessions`
  MODIFY `session_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=139;

--
-- AUTO_INCREMENT for table `taps`
--
ALTER TABLE `taps`
  MODIFY `tap_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bar_access`
--
ALTER TABLE `bar_access`
  ADD CONSTRAINT `cascade_bars_on_bar_access` FOREIGN KEY (`fk_bar_id`) REFERENCES `bars` (`bar_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `cascade_users_on_bar_access` FOREIGN KEY (`fk_user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `beers`
--
ALTER TABLE `beers`
  ADD CONSTRAINT `brewery_on_fk_brewery` FOREIGN KEY (`fk_brewery_id`) REFERENCES `breweries` (`brewery_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `set_null_user_on_created_by` FOREIGN KEY (`fk_beer_created_by`) REFERENCES `users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `set_null_user_on_updated_by` FOREIGN KEY (`fk_beer_updated_by`) REFERENCES `users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `style_on_fk_style` FOREIGN KEY (`fk_beer_style_id`) REFERENCES `beer_styles` (`beer_style_id`) ON UPDATE CASCADE;

--
-- Constraints for table `pizzas`
--
ALTER TABLE `pizzas`
  ADD CONSTRAINT `cascade_bar_on_fk_bar` FOREIGN KEY (`fk_bar_id`) REFERENCES `bars` (`bar_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `pizza_ingredients`
--
ALTER TABLE `pizza_ingredients`
  ADD CONSTRAINT `cascade_pizza_on_fk_pizza` FOREIGN KEY (`fk_pizza_id`) REFERENCES `pizzas` (`pizza_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ingredient_on_fk_ingredient` FOREIGN KEY (`fk_ingredient_id`) REFERENCES `ingredients` (`ingredient_id`) ON UPDATE CASCADE;

--
-- Constraints for table `sessions`
--
ALTER TABLE `sessions`
  ADD CONSTRAINT `cascade_user_on_session_user_id` FOREIGN KEY (`fk_user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `taps`
--
ALTER TABLE `taps`
  ADD CONSTRAINT `cascade_bars_on_taps` FOREIGN KEY (`fk_bar_id`) REFERENCES `bars` (`bar_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `cascade_beers_on_taps` FOREIGN KEY (`fk_beer_id`) REFERENCES `beers` (`beer_id`) ON UPDATE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `user_role_on_user` FOREIGN KEY (`fk_user_role_id`) REFERENCES `user_roles` (`user_role_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
