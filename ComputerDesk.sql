-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 15, 2021 at 12:20 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `computerdesk`
--

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(128) NOT NULL,
  `code` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `icon` varchar(128) NOT NULL,
  `price` int(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `code`, `name`, `icon`, `price`) VALUES
(1, 'PRODUCT10', 'Karbantartás', 'fas fa-wrench', 8000),
(2, 'PRODUCT11', 'Adatmentés', 'fas fa-chart-pie', 20000),
(3, 'PRODUCT12', 'Távoli segítségnyújtás', 'fas fa-phone-alt', 6000),
(5, 'PRODUCT13', 'Számítógép tisztítás', 'fas fa-magic', 12500),
(6, 'PRODUCT14', 'Szervízelés szállítással', 'fas fa-truck-loading', 10000),
(7, 'PRODUCT15', 'Windows telepítése', 'fab fa-windows', 15000),
(8, 'PRODUCT16', 'Bővítés, fejlesztés', 'fas fa-rocket', 20000),
(9, 'PRODUCT17', 'Kijelző fóliázás', 'fas fa-mobile-alt', 6500),
(10, 'PRODUCT18', 'Laptop vásárlás', 'fas fa-laptop', 30000),
(11, 'PRODUCT19', 'Konfigurálás', 'fas fa-cog', 15000),
(12, 'PRODUCT20', 'Hálozat kiépítés', 'fas fa-wifi', 26000);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `usersId` int(128) NOT NULL,
  `usersUid` varchar(128) NOT NULL,
  `usersName` varchar(128) NOT NULL,
  `usersEmail` varchar(128) NOT NULL,
  `usersPwd` varchar(128) NOT NULL,
  `regDate` varchar(128) NOT NULL,
  `admin` int(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`usersId`, `usersUid`, `usersName`, `usersEmail`, `usersPwd`, `regDate`, `admin`) VALUES
(1, 'admin', 'Várnai Dávid', 'varnaidavid0522@gmail.com', '$2b$12$P0lfpurjvLGT6mCR3vEYPe8fdT3USRkPdHfubQp.U/ODM20m6ZoHa', '10. December 2020, 22:54', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`usersId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(128) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `usersId` int(128) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
