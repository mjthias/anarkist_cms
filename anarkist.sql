-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: May 09, 2023 at 11:01 AM
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
(1, 'Anarkist Bar', 'Bernstorffsgade 7', '1786', 'København V'),
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
(1, 2),
(2, 2),
(1, 3);

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
(1, 'American Haze', 1, '20', '15', '4,0', 2, 55, '', 'Nice beer', 'God øl', 1683627451, 3, 1683627451, 3),
(2, 'Great Grandpa', 2, '50', '15', '5,2', 1, 75, '', 'Very nice beer', 'Rigtig god øl', 1683627451, 2, 1683627451, 2);

-- --------------------------------------------------------

--
-- Table structure for table `beer_styles`
--

CREATE TABLE `beer_styles` (
  `beer_style_id` bigint(20) UNSIGNED NOT NULL,
  `beer_style_title` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `beer_styles`
--

INSERT INTO `beer_styles` (`beer_style_id`, `beer_style_title`) VALUES
(2, 'Hazy IPA'),
(1, 'IPA'),
(3, 'Sour');

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
(1, 'Anarkist', 'Anarkist'),
(2, 'Too Old To Die Young', 'TOTDY');

-- --------------------------------------------------------

--
-- Table structure for table `ingredients`
--

CREATE TABLE `ingredients` (
  `ingredient_id` bigint(20) UNSIGNED NOT NULL,
  `ingredient_name_en` varchar(50) NOT NULL,
  `ingredient_name_dk` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ingredients`
--

INSERT INTO `ingredients` (`ingredient_id`, `ingredient_name_en`, `ingredient_name_dk`) VALUES
(1, 'Onion', 'Løg'),
(2, 'Rosemary', 'Rosmarin');

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

--
-- Dumping data for table `pizzas`
--

INSERT INTO `pizzas` (`pizza_id`, `pizza_name`, `pizza_number`, `fk_bar_id`) VALUES
(1, 'Nasty Rosy', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `pizza_ingredients`
--

CREATE TABLE `pizza_ingredients` (
  `fk_pizza_id` bigint(20) UNSIGNED NOT NULL,
  `fk_ingredient_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `pizza_ingredients`
--

INSERT INTO `pizza_ingredients` (`fk_pizza_id`, `fk_ingredient_id`) VALUES
(1, 1),
(1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `session_id` bigint(20) UNSIGNED NOT NULL,
  `fk_user_id` bigint(20) UNSIGNED NOT NULL,
  `session_iat` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
(10, 1, 1, 1, 0),
(11, 2, 2, 1, 0),
(12, NULL, 2, 1, 0),
(13, NULL, 1, 1, 0),
(14, 1, 2, 2, 0);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `user_password` varchar(50) NOT NULL,
  `fk_user_role_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_email`, `user_name`, `user_password`, `fk_user_role_id`) VALUES
(1, 'super@user.dk', 'Super User', 'ASDasd123!', 1),
(2, 'bar@admin.dk', 'Bar Admin', 'ASDasd123!', 2),
(3, 'bar@staff.dk', 'Bar Staff', 'ASDasd123!', 3);

-- --------------------------------------------------------

--
-- Table structure for table `user_roles`
--

CREATE TABLE `user_roles` (
  `user_role_id` bigint(20) UNSIGNED NOT NULL,
  `user_role_title` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_roles`
--

INSERT INTO `user_roles` (`user_role_id`, `user_role_title`) VALUES
(1, 'superuser'),
(2, 'bar admin'),
(3, 'bar staff');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bars`
--
ALTER TABLE `bars`
  ADD PRIMARY KEY (`bar_id`);

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
  ADD KEY `brewery_on_fk_brewery` (`fk_brewery_id`),
  ADD KEY `style_on_fk_style` (`fk_beer_style_id`),
  ADD KEY `set_null_user_on_created_by` (`fk_beer_created_by`),
  ADD KEY `set_null_user_on_updated_by` (`fk_beer_updated_by`);

--
-- Indexes for table `beer_styles`
--
ALTER TABLE `beer_styles`
  ADD PRIMARY KEY (`beer_style_id`),
  ADD UNIQUE KEY `beer_style_title` (`beer_style_title`);

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
  MODIFY `bar_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `beers`
--
ALTER TABLE `beers`
  MODIFY `beer_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `beer_styles`
--
ALTER TABLE `beer_styles`
  MODIFY `beer_style_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `breweries`
--
ALTER TABLE `breweries`
  MODIFY `brewery_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

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
  MODIFY `session_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `taps`
--
ALTER TABLE `taps`
  MODIFY `tap_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user_roles`
--
ALTER TABLE `user_roles`
  MODIFY `user_role_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

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
  ADD CONSTRAINT `brewery_on_fk_brewery` FOREIGN KEY (`fk_brewery_id`) REFERENCES `breweries` (`brewery_id`) ON UPDATE CASCADE,
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
  ADD CONSTRAINT `cascade_beers_on_taps` FOREIGN KEY (`fk_beer_id`) REFERENCES `beers` (`beer_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `user_role_on_user` FOREIGN KEY (`fk_user_role_id`) REFERENCES `user_roles` (`user_role_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
