-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2+deb7u1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 05, 2015 at 09:42 AM
-- Server version: 5.5.41
-- PHP Version: 5.4.36-0+deb7u3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `PlashBoard`
--
CREATE DATABASE `PlashBoard` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `PlashBoard`;

-- --------------------------------------------------------

--
-- Table structure for table `hardwareConfiguration`
--

CREATE TABLE IF NOT EXISTS `hardwareConfiguration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `pin` tinyint(2) NOT NULL,
  `type` enum('Analog','Numeric','','') NOT NULL,
  `IO` enum('Input','Output','','') NOT NULL,
  `PullUpDownResistor` enum('None','Pull-Up','Pull-Down','') NOT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `tension` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `hardwareConfiguration`
--

INSERT INTO `hardwareConfiguration` (`id`, `name`, `pin`, `type`, `IO`, `PullUpDownResistor`, `unit`, `tension`) VALUES
(1, 'Pool Temperature Sensor', 1, 'Analog', 'Input', 'None', '°c', NULL),
(2, 'Pool Light', 1, 'Numeric', 'Output', 'None', NULL, 5),
(3, 'Pump Ampere Meter', 3, 'Analog', 'Input', 'None', 'A', NULL),
(4, 'Pool Ph Meter', 4, 'Analog', 'Input', 'None', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `measure`
--

CREATE TABLE IF NOT EXISTS `measure` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hardwareConfigurationId` int(11) NOT NULL,
  `value` float NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hardwareConfiguration` (`hardwareConfigurationId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=295470 ;

-- --------------------------------------------------------

--
-- Table structure for table `userCommand`
--

CREATE TABLE IF NOT EXISTS `userCommand` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` enum('UserCommand','Actuators') NOT NULL,
  `command` enum('Create','Update','Delete','Get','Set') NOT NULL,
  `targetName` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `done` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- Table structure for table `userConfiguration`
--

CREATE TABLE IF NOT EXISTS `userConfiguration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `hardwareConfigurationId` int(11) NOT NULL,
  `unit` varchar(50) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hardwareConfiguration` (`hardwareConfigurationId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `measure`
--
ALTER TABLE `measure`
  ADD CONSTRAINT `hardwareConfiguration` FOREIGN KEY (`hardwareConfigurationId`) REFERENCES `hardwareConfiguration` (`id`);

--
-- Constraints for table `userConfiguration`
--
ALTER TABLE `userConfiguration`
  ADD CONSTRAINT `hardwareConfigurationId` FOREIGN KEY (`hardwareConfigurationId`) REFERENCES `hardwareConfiguration` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
