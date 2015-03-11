-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Client :  127.0.0.1
-- Généré le :  Mer 11 Mars 2015 à 14:15
-- Version du serveur :  5.6.17
-- Version de PHP :  5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données :  `plashboard`
--
CREATE DATABASE IF NOT EXISTS `plashboard` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `plashboard`;

-- --------------------------------------------------------

--
-- Structure de la table `hardwareconfiguration`
--

CREATE TABLE IF NOT EXISTS `hardwareconfiguration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `pin` tinyint(2) NOT NULL,
  `type` enum('Analog','Numeric','','') NOT NULL,
  `IO` enum('Input','Output','','') NOT NULL,
  `PullUpDownResistor` enum('None','Pull-Up','Pull-Down','') NOT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `tension` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Contenu de la table `hardwareconfiguration`
--

INSERT INTO `hardwareconfiguration` (`id`, `name`, `pin`, `type`, `IO`, `PullUpDownResistor`, `unit`, `tension`) VALUES
(1, 'Pool Temperature Sensor', 1, 'Analog', 'Input', 'None', '°C', NULL),
(2, 'Pool Light', 1, 'Numeric', 'Output', 'Pull-Down', NULL, 5),
(3, 'Pump Ampere Meter', 2, 'Analog', 'Input', 'None', 'A', NULL),
(4, 'Pool Ph Meter', 3, 'Analog', 'Input', 'None', NULL, NULL),
(5, 'Pool Pump', 2, 'Numeric', 'Output', 'None', 'Null', 5),
(6, 'Pool Heater', 3, 'Numeric', 'Output', 'None', 'Null', 5);

-- --------------------------------------------------------

--
-- Structure de la table `measure`
--

CREATE TABLE IF NOT EXISTS `measure` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hardwareConfigurationId` int(11) NOT NULL,
  `value` float NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hardwareConfiguration` (`hardwareConfigurationId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Contenu de la table `measure`
--

INSERT INTO `measure` (`id`, `hardwareConfigurationId`, `value`, `timestamp`) VALUES
(1, 1, 12, '2015-03-05 07:00:00'),
(2, 1, 13, '2015-03-05 07:27:00');

-- --------------------------------------------------------

--
-- Structure de la table `usercommand`
--

CREATE TABLE IF NOT EXISTS `usercommand` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` enum('UserConfiguration','Actuators') NOT NULL,
  `command` enum('Create','Update','Delete','Get','Set') NOT NULL,
  `targetName` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `done` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Contenu de la table `usercommand`
--

INSERT INTO `usercommand` (`id`, `type`, `command`, `targetName`, `value`, `timestamp`, `done`) VALUES
(1, 'Actuators', 'Set', 'Pool Light', '1', '2015-03-05 16:00:00', 1),
(2, 'Actuators', 'Set', 'Pool Light', '0', '2015-03-05 17:00:00', 0);

-- --------------------------------------------------------

--
-- Structure de la table `userconfiguration`
--

CREATE TABLE IF NOT EXISTS `userconfiguration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `hardwareConfigurationId` int(11) NOT NULL,
  `unit` varchar(50) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hardwareConfiguration` (`hardwareConfigurationId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Contenu de la table `userconfiguration`
--

INSERT INTO `userconfiguration` (`id`, `name`, `hardwareConfigurationId`, `unit`, `value`) VALUES
(1, 'Ph', 4, 'None', '7'),
(2, 'Temperature', 1, '°C', '22');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Contenu de la table `users`
--

INSERT INTO `users` (`id`, `name`, `password`) VALUES
(1, 'root', 'root'),
(2, 'user', 'password');

--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `measure`
--
ALTER TABLE `measure`
  ADD CONSTRAINT `hardwareConfiguration` FOREIGN KEY (`hardwareConfigurationId`) REFERENCES `hardwareconfiguration` (`id`);

--
-- Contraintes pour la table `userconfiguration`
--
ALTER TABLE `userconfiguration`
  ADD CONSTRAINT `hardwareConfigurationId` FOREIGN KEY (`hardwareConfigurationId`) REFERENCES `hardwareconfiguration` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
