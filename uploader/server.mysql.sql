SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";
CREATE DATABASE IF NOT EXISTS `videoag` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `videoag`;

DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth` (
`id` smallint(6) NOT NULL,
  `token` char(128) NOT NULL,
  `user` tinytext NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `valid` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `fileevent`;
CREATE TABLE `fileevent` (
`id` mediumint(8) unsigned NOT NULL,
  `file` mediumint(8) unsigned NOT NULL,
  `lecture` mediumint(5) unsigned NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `files`;
CREATE TABLE `files` (
`id` mediumint(8) unsigned NOT NULL,
  `uuhash` tinytext NOT NULL,
  `origname` tinytext NOT NULL,
  `path` text,
  `size` bigint(20) unsigned NOT NULL,
  `mtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `md5` char(32) DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;


ALTER TABLE `auth`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `token` (`token`);

ALTER TABLE `fileevent`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `filelecture` (`file`,`lecture`), ADD KEY `fileevent` (`file`), ADD KEY `lecture` (`lecture`);

ALTER TABLE `files`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `uuhash` (`uuhash`(255));


ALTER TABLE `auth`
MODIFY `id` smallint(6) NOT NULL AUTO_INCREMENT;
ALTER TABLE `fileevent`
MODIFY `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE `files`
MODIFY `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT;
