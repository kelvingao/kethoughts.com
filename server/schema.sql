-- MIT License
--
-- Copyright (c) 2019 Kelvin Gao
--
-- Permission is hereby granted, free of charge, to any person obtaining a copy
-- of this software and associated documentation files (the "Software"), to deal
-- in the Software without restriction, including without limitation the rights
-- to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
-- copies of the Software, and to permit persons to whom the Software is
-- furnished to do so, subject to the following conditions:
--
-- The above copyright notice and this permission notice shall be included in all
-- copies or substantial portions of the Software.
--
-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
-- IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
-- FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
-- AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
-- LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
-- OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
-- SOFTWARE.

-- To create the database:
--   CREATE DATABASE kethoughts_db;
--   CREATE USER 'kethoughts_user'@'localhost' IDENTIFIED BY 'kethoughts_pass';
--   GRANT ALL PRIVILEGES ON kethoughts_db. * TO 'kethoughts_user'@'localhost';

-- To reload the tables:
--   mysql -u kethoughts_user -p kethoughts_db < schema.sql

SET foreign_key_checks = 0;

CREATE TABLE IF NOT EXISTS `kt_users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(64) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`email`),
  KEY `created` (`created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS `kt_posts` (
  `id` int(11) unsigned AUTO_INCREMENT,
  `author_id` int(11) unsigned DEFAULT 0,
  `slug` varchar(100),
  `title` varchar(100),
  `excerpt` text,
  `content` longtext,
  `status` tinyint unsigned DEFAULT 1,
  `type` tinyint unsigned DEFAULT 1,
  `comment_count` bigint unsigned DEFAULT 0,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`slug`),
  KEY `created` (`created`),
  KEY `modified` (`modified`),
  CONSTRAINT `post_user` FOREIGN KEY (`author_id`) REFERENCES `kt_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

SET foreign_key_checks = 1;