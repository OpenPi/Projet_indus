-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Client :  127.0.0.1
-- Généré le :  Jeu 05 Mars 2015 à 11:17
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Contenu de la table `hardwareconfiguration`
--

INSERT INTO `hardwareconfiguration` (`id`, `name`, `pin`, `type`, `IO`, `PullUpDownResistor`, `unit`, `tension`) VALUES
(1, 'Pool Temperature Sensor', 1, 'Analog', 'Input', 'None', '°c', NULL),
(2, 'Pool Light', 1, 'Numeric', 'Output', 'None', NULL, 5),
(3, 'Pump Ampere Meter', 3, 'Analog', 'Input', 'None', 'A', NULL),
(4, 'Pool Ph Meter', 4, 'Analog', 'Input', 'None', NULL, NULL);

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

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
