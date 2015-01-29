BEGIN;
CREATE TABLE `cards_catalog` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(255) NOT NULL,
    `slug` varchar(50) NOT NULL UNIQUE,
    `description` longtext NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `is_alpha` bool NOT NULL
)
;
CREATE TABLE `cards_signum` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(255) NOT NULL,
    `description` longtext NOT NULL,
    `slug` varchar(50) NOT NULL UNIQUE
)
;
CREATE TABLE `cards_box` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `folder_name` varchar(255) NOT NULL UNIQUE,
    `sequence_number` integer NOT NULL,
    `slug` varchar(50) NOT NULL UNIQUE,
    `label` varchar(255) NOT NULL,
    `catalog_id` integer NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL
)
;
ALTER TABLE `cards_box` ADD CONSTRAINT `catalog_id_refs_id_85916995` FOREIGN KEY (`catalog_id`) REFERENCES `cards_catalog` (`id`);
CREATE TABLE `cards_card` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(255) NOT NULL,
    `filename` varchar(255) NOT NULL,
    `ocr_text` longtext NOT NULL,
    `letter` varchar(1),
    `sequence_number` integer NOT NULL,
    `catalog_sequence_number` integer,
    `box_id` integer NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `signum_id` integer,
    `name_tr` varchar(255),
    `arr_tr` varchar(255),
    `pseudonym_tr` varchar(255),
    `title_tr` varchar(255),
    `comment` longtext
)
;
ALTER TABLE `cards_card` ADD CONSTRAINT `box_id_refs_id_c7dfed04` FOREIGN KEY (`box_id`) REFERENCES `cards_box` (`id`);
ALTER TABLE `cards_card` ADD CONSTRAINT `signum_id_refs_id_bb011d5a` FOREIGN KEY (`signum_id`) REFERENCES `cards_signum` (`id`);
CREATE INDEX `cards_signum_4da47e07` ON `cards_signum` (`name`);
CREATE INDEX `cards_box_03af850d` ON `cards_box` (`sequence_number`);
CREATE INDEX `cards_box_e05256b6` ON `cards_box` (`label`);
CREATE INDEX `cards_box_99260dd6` ON `cards_box` (`catalog_id`);
CREATE INDEX `cards_card_4da47e07` ON `cards_card` (`name`);
CREATE INDEX `cards_card_606e157c` ON `cards_card` (`filename`);
CREATE INDEX `cards_card_45f341a0` ON `cards_card` (`letter`);
CREATE INDEX `cards_card_03af850d` ON `cards_card` (`sequence_number`);
CREATE INDEX `cards_card_cdd9e3d2` ON `cards_card` (`box_id`);
CREATE INDEX `cards_card_16247eed` ON `cards_card` (`signum_id`);
CREATE INDEX `cards_card_ac47477f` ON `cards_card` (`name_tr`);
CREATE INDEX `cards_card_db0b739f` ON `cards_card` (`arr_tr`);
CREATE INDEX `cards_card_85c5b096` ON `cards_card` (`pseudonym_tr`);
CREATE INDEX `cards_card_a15ea0d1` ON `cards_card` (`title_tr`);

COMMIT;
