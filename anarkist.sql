-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: May 09, 2023 at 07:01 AM
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

-- --------------------------------------------------------

--
-- Table structure for table `bar_access`
--

CREATE TABLE `bar_access` (
  `fk_bar_id` bigint(20) UNSIGNED NOT NULL,
  `fk_user_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `beers`
--

CREATE TABLE `beers` (
  `beer_id` bigint(20) UNSIGNED NOT NULL,
  `beer_name` varchar(50) NOT NULL,
  `fk_brewery_id` bigint(20) UNSIGNED NOT NULL,
  `beer_ebc` varchar(3) DEFAULT NULL,
  `beer_ibu` varchar(3) NOT NULL,
  `beer_alc` varchar(5) NOT NULL,
  `fk_beer_style_id` bigint(20) UNSIGNED NOT NULL,
  `beer_price` double UNSIGNED NOT NULL,
  `beer_image` varchar(41) NOT NULL,
  `beer_description_en` varchar(500) NOT NULL,
  `beer_description_dk` varchar(500) NOT NULL,
  `beer_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fk_beer_created_by` bigint(20) UNSIGNED NOT NULL,
  `beer_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fk_beer_updated_by` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `beer_styles`
--

CREATE TABLE `beer_styles` (
  `beer_style_id` bigint(20) UNSIGNED NOT NULL,
  `beer_style_title` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `breweries`
--

CREATE TABLE `breweries` (
  `brewery_id` bigint(20) UNSIGNED NOT NULL,
  `brewery_name` varchar(100) NOT NULL,
  `brewery_menu_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
  `fk_user_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `taps`
--

CREATE TABLE `taps` (
  `tap_id` bigint(20) UNSIGNED NOT NULL,
  `tap_number` tinyint(100) DEFAULT NULL,
  `fk_beer_id` bigint(20) UNSIGNED NOT NULL,
  `tap_off_the_wall` tinyint(1) NOT NULL,
  `fk_bar_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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

-- --------------------------------------------------------

--
-- Table structure for table `user_roles`
--

CREATE TABLE `user_roles` (
  `user_role_id` bigint(20) UNSIGNED NOT NULL,
  `user_role_title` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bars`
--
ALTER TABLE `bars`
  ADD PRIMARY KEY (`bar_id`),
  ADD UNIQUE KEY `bar_id` (`bar_id`);

--
-- Indexes for table `bar_access`
--
ALTER TABLE `bar_access`
  ADD PRIMARY KEY (`fk_bar_id`,`fk_user_id`);

--
-- Indexes for table `beers`
--
ALTER TABLE `beers`
  ADD PRIMARY KEY (`beer_id`),
  ADD UNIQUE KEY `beer_id` (`beer_id`);

--
-- Indexes for table `beer_styles`
--
ALTER TABLE `beer_styles`
  ADD PRIMARY KEY (`beer_style_id`),
  ADD UNIQUE KEY `beer_style_id` (`beer_style_id`);

--
-- Indexes for table `breweries`
--
ALTER TABLE `breweries`
  ADD PRIMARY KEY (`brewery_id`),
  ADD UNIQUE KEY `brewery_id` (`brewery_id`);

--
-- Indexes for table `ingredients`
--
ALTER TABLE `ingredients`
  ADD PRIMARY KEY (`ingredient_id`),
  ADD UNIQUE KEY `ingredient_id` (`ingredient_id`);

--
-- Indexes for table `pizzas`
--
ALTER TABLE `pizzas`
  ADD PRIMARY KEY (`pizza_id`),
  ADD UNIQUE KEY `pizza_id` (`pizza_id`),
  ADD UNIQUE KEY `pizza_number` (`pizza_number`);

--
-- Indexes for table `pizza_ingredients`
--
ALTER TABLE `pizza_ingredients`
  ADD PRIMARY KEY (`fk_pizza_id`,`fk_ingredient_id`);

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`session_id`),
  ADD UNIQUE KEY `session_id` (`session_id`);

--
-- Indexes for table `taps`
--
ALTER TABLE `taps`
  ADD PRIMARY KEY (`tap_id`),
  ADD UNIQUE KEY `tap_id` (`tap_id`),
  ADD UNIQUE KEY `tap_number` (`tap_number`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`user_role_id`),
  ADD UNIQUE KEY `user_role_id` (`user_role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bars`
--
ALTER TABLE `bars`
  MODIFY `bar_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `beers`
--
ALTER TABLE `beers`
  MODIFY `beer_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `beer_styles`
--
ALTER TABLE `beer_styles`
  MODIFY `beer_style_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `breweries`
--
ALTER TABLE `breweries`
  MODIFY `brewery_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ingredients`
--
ALTER TABLE `ingredients`
  MODIFY `ingredient_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pizzas`
--
ALTER TABLE `pizzas`
  MODIFY `pizza_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sessions`
--
ALTER TABLE `sessions`
  MODIFY `session_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `taps`
--
ALTER TABLE `taps`
  MODIFY `tap_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_roles`
--
ALTER TABLE `user_roles`
  MODIFY `user_role_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
