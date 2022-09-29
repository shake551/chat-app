CREATE TABLE `accounts_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(240) NOT NULL,
  `password` varchar(255) NOT NULL,
  `salt` varchar(255) NOT NULL,
  `urltoken` char(32) NOT NULL,
  `status` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `chat_room` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `member_count` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `chat_roommember` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `room_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chat_roommember_room_id_db53f589_fk_chat_room_id` (`room_id`),
  KEY `chat_roommember_user_id_3cf07995_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `chat_roommember_room_id_db53f589_fk_chat_room_id` FOREIGN KEY (`room_id`) REFERENCES `chat_room` (`id`),
  CONSTRAINT `chat_roommember_user_id_3cf07995_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `chat_roommessage` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `message` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `room_id` bigint(20) NOT NULL,
  `send_user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chat_roommessage_room_id_20538a80_fk_chat_room_id` (`room_id`),
  KEY `chat_roommessage_send_user_id_fe4865e8_fk_accounts_user_id` (`send_user_id`),
  CONSTRAINT `chat_roommessage_room_id_20538a80_fk_chat_room_id` FOREIGN KEY (`room_id`) REFERENCES `chat_room` (`id`),
  CONSTRAINT `chat_roommessage_send_user_id_fe4865e8_fk_accounts_user_id` FOREIGN KEY (`send_user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
