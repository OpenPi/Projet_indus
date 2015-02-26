-- phpMyAdmin SQL Dump
-- version 4.2.5
-- http://www.phpmyadmin.net
--
-- Client :  localhost:8889
-- Généré le :  Mar 24 Février 2015 à 13:17
-- Version du serveur :  5.5.38
-- Version de PHP :  5.5.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Base de données :  `PlashBoard`
--
CREATE DATABASE IF NOT EXISTS `PlashBoard` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `PlashBoard`;

-- --------------------------------------------------------

--
-- Structure de la table `hardwareConfiguration`
--

CREATE TABLE `hardwareConfiguration` (
`id` int(11) NOT NULL,
  `hardwareName` varchar(255) NOT NULL,
  `pin` tinyint(2) NOT NULL,
  `type` enum('Analog','Numeric','','') NOT NULL,
  `IO` enum('Input','Output','','') NOT NULL,
  `PullUpDownResistor` enum('None','Pull-Up','Pull-Down','') NOT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `tension` float DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- Structure de la table `measure`
--

CREATE TABLE `measure` (
`id` int(11) NOT NULL,
  `hardwareConfigurationId` int(11) NOT NULL,
  `value` float NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

-- --------------------------------------------------------

--
-- Structure de la table `userCommand`
--

CREATE TABLE `userCommand` (
`id` int(11) NOT NULL,
  `command` enum('Create','Update','Delete','Get','Set') NOT NULL,
  `targetName` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `done` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Structure de la table `userConfiguration`
--

CREATE TABLE `userConfiguration` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `hardwareConfigurationId` int(11) NOT NULL,
  `unit` varchar(50) NOT NULL,
  `value` varchar(255) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Index pour les tables exportées
--

--
-- Index pour la table `hardwareConfiguration`
--
ALTER TABLE `hardwareConfiguration`
 ADD PRIMARY KEY (`id`);

--
-- Index pour la table `measure`
--
ALTER TABLE `measure`
 ADD PRIMARY KEY (`id`), ADD KEY `hardwareConfiguration` (`hardwareConfigurationId`);

--
-- Index pour la table `userCommand`
--
ALTER TABLE `userCommand`
 ADD PRIMARY KEY (`id`);

--
-- Index pour la table `userConfiguration`
--
ALTER TABLE `userConfiguration`
 ADD PRIMARY KEY (`id`), ADD KEY `hardwareConfiguration` (`hardwareConfigurationId`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `hardwareConfiguration`
--
ALTER TABLE `hardwareConfiguration`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT pour la table `measure`
--
ALTER TABLE `measure`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT pour la table `userCommand`
--
ALTER TABLE `userCommand`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `userConfiguration`
--
ALTER TABLE `userConfiguration`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `measure`
--
ALTER TABLE `measure`
ADD CONSTRAINT `hardwareConfiguration` FOREIGN KEY (`hardwareConfigurationId`) REFERENCES `hardwareConfiguration` (`id`);

--
-- Contraintes pour la table `userConfiguration`
--
ALTER TABLE `userConfiguration`
ADD CONSTRAINT `hardwareConfigurationId` FOREIGN KEY (`hardwareConfigurationId`) REFERENCES `hardwareConfiguration` (`id`);
