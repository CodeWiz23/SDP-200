-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 31, 2024 at 01:56 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sdp_200`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `booking_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `room_number` int(11) NOT NULL,
  `payment_method` enum('Credit Card','Cash','Bank Transfer') NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `currency` enum('USD','TK') NOT NULL,
  `status` enum('Confirmed','Cancelled') NOT NULL DEFAULT 'Confirmed',
  `booking_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`booking_id`, `user_id`, `room_number`, `payment_method`, `amount`, `currency`, `status`, `booking_date`) VALUES
(5, 1, 6, '', 200.00, 'TK', 'Confirmed', '2024-12-31 12:10:15');

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `employee_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `role` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `salary` decimal(10,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`employee_id`, `name`, `role`, `email`, `phone`, `salary`, `created_at`, `updated_at`) VALUES
(1, 'a', 'a', 'a', 'a', 0.00, '2024-12-31 08:17:39', '2024-12-31 08:17:39'),
(2, 'Z', 'Z', 'Z', 'Z', 0.00, '2024-12-31 12:49:37', '2024-12-31 12:49:37');

-- --------------------------------------------------------

--
-- Table structure for table `extra_services`
--

CREATE TABLE `extra_services` (
  `service_id` int(11) NOT NULL,
  `service_name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `extra_services`
--

INSERT INTO `extra_services` (`service_id`, `service_name`, `description`, `price`, `created_at`, `updated_at`) VALUES
(1, 'Spa', 'Relaxing spa treatment', 50.00, '2024-12-31 08:14:52', '2024-12-31 08:14:52'),
(2, 'Gym Access', 'Access to the hotel gym', 20.00, '2024-12-31 08:14:52', '2024-12-31 08:14:52'),
(3, 'Airport Transfer', 'Transportation to and from the airport', 30.00, '2024-12-31 08:14:52', '2024-12-31 08:14:52'),
(4, 'Breakfast', 'Continental breakfast served in your room', 15.00, '2024-12-31 08:14:52', '2024-12-31 08:14:52'),
(5, 'Late Check-out', 'Extend your check-out time by 2 hours', 25.00, '2024-12-31 08:14:52', '2024-12-31 08:14:52'),
(6, 'a', '1', 100.00, '2024-12-31 08:17:27', '2024-12-31 08:17:27'),
(7, 'Z', 'Z', 11.00, '2024-12-31 12:49:18', '2024-12-31 12:49:18');

-- --------------------------------------------------------

--
-- Table structure for table `extra_service_bookings`
--

CREATE TABLE `extra_service_bookings` (
  `booking_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `payment_method` enum('Credit Card','Cash','Bank Transfer') NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `currency` enum('USD','TK') NOT NULL,
  `status` enum('Confirmed','Cancelled') DEFAULT 'Confirmed',
  `booking_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `hotel_policy`
--

CREATE TABLE `hotel_policy` (
  `policy_id` int(11) NOT NULL,
  `policy_description` text NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hotel_policy`
--

INSERT INTO `hotel_policy` (`policy_id`, `policy_description`, `updated_at`) VALUES
(1, 'Hotel Policies\n\n\n\n\nCheck-in and Check-out\nCheck-in Time: 3:00 PM or later.\nCheck-out Time: 11:00 AM.\nEarly check-in or late check-out may be arranged based on room availability and may incur additional charges.\nCancellation and Refund Policy\nStandard Cancellation: Cancellations made at least 48 hours before the check-in date will receive a full refund.\nLate Cancellation: Cancellations made within 48 hours of the check-in date will be charged a 50% cancellation fee.\nNo-Show: If you do not arrive for your booking, no refund will be issued.\nSmoking Policy\nNon-Smoking Property: Our hotel is a non-smoking property. Smoking is prohibited in all indoor areas including rooms, hallways, and public spaces. Designated smoking areas are available outside the property.\nPenalty for Smoking in Rooms: A cleaning fee of $250 will be charged if smoking occurs in a room.\nPets Policy\nPets Allowed: We welcome small pets (under 20 lbs) for an additional fee of $50 per stay.\nPet-Free Zones: Pets are not allowed in restaurants, spa areas, or poolside areas.\nService Animals: Service animals are permitted without additional charges.\nPayment Policy\nAccepted Payment Methods: We accept all major credit cards including Visa, MasterCard, American Express, and Discover. Payments can also be made via PayPal.\nSecurity Deposit: A refundable security deposit of $100 per stay is required upon check-in. The deposit will be refunded after a room inspection upon check-out, provided there is no damage or violation of hotel policies.\nTaxes: All rates are subject to applicable taxes and fees.\nNoise and Behavior\nNoise Restrictions: To maintain a comfortable environment for all guests, quiet hours are enforced from 10:00 PM to 8:00 AM. Excessive noise or disruptive behavior will not be tolerated.\nAlcohol Consumption: Alcoholic beverages may be consumed only in designated areas such as the bar or restaurant. Outside alcohol is not allowed in public spaces.\nLost and Found\nGuest Responsibility: Guests are encouraged to keep personal items secure. The hotel is not responsible for lost, stolen, or damaged items.\nLost Items: Any lost items found during your stay will be stored for 30 days. After 30 days, unclaimed items will be donated or discarded.\nSafety and Security\nEmergency Exits: Emergency exits are clearly marked in all rooms and public areas. Please familiarize yourself with the location of exits during your stay.\nSecurity Services: The hotel is monitored 24/7 by security cameras. For your safety, please lock your room door when leaving the room and during the night.\nHealth and Safety\nCOVID-19 Guidelines: We follow all local health protocols regarding COVID-19, including regular sanitation of high-touch areas, mask requirements in indoor spaces, and social distancing in public areas.\nMedical Assistance: A first aid kit is available at the front desk. For emergencies, dial 911 or contact the front desk for assistance.\nSpecial Requests\nRoom Preferences: While we will do our best to accommodate special requests such as room type, bedding preferences, or accessibility needs, all requests are subject to availability and may incur additional charges.\nDamage to Property\nGuest Responsibility: Guests are responsible for any damage caused to hotel property during their stay. Charges will apply for the repair or replacement of damaged items.\nExcessive Cleaning: A fee may be charged for rooms requiring excessive cleaning due to stains, spills, or other damage beyond normal use.\nSwimming Pool and Gym\nPool Hours: The pool is open from 8:00 AM to 10:00 PM. No lifeguard is on duty. Swimming is at your own risk.\nGym Hours: The gym is open 24 hours a day. Proper attire must be worn at all times.\nGuest Behavior and Hotel Conduct\nRespectful Behavior: All guests are expected to behave in a courteous and respectful manner. The hotel reserves the right to refuse service to any guest exhibiting inappropriate or disruptive behavior.\nHotel Right to Refuse Service: The hotel reserves the right to refuse service or evict any guest without refund who violates hotel policies, causes damage, or disrupts the comfort of other guests.\nPrivacy and Data Protection\nData Collection: The hotel collects personal information such as name, address, and payment details for booking purposes. We are committed to protecting your privacy and will not share your data without your consent.\nSecurity of Personal Information: All payment and personal details are handled with the utmost security, and the hotel complies with all relevant data protection laws.\nThis comprehensive hotel policy covers a wide range of aspects, including guest conduct, payments, cancellations, pets, safety, and privacy. You can tailor the policy to your specific needs by adjusting the terms, fees, and conditions as necessary.', '2024-12-31 09:46:45');

-- --------------------------------------------------------

--
-- Table structure for table `packages`
--

CREATE TABLE `packages` (
  `package_id` int(11) NOT NULL,
  `package_name` varchar(255) NOT NULL,
  `original_price` decimal(10,2) NOT NULL,
  `discount_percentage` decimal(5,2) NOT NULL,
  `discounted_price` decimal(10,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `packages`
--

INSERT INTO `packages` (`package_id`, `package_name`, `original_price`, `discount_percentage`, `discounted_price`, `created_at`, `updated_at`) VALUES
(1, 'Weekend Getaway', 300.00, 10.00, 270.00, '2024-12-31 08:14:52', '2024-12-31 08:14:52'),
(2, 'Romantic Escape', 400.00, 15.00, 340.00, '2024-12-31 08:14:52', '2024-12-31 08:14:52'),
(3, 'Business Stay', 500.00, 5.00, 475.00, '2024-12-31 08:14:52', '2024-12-31 08:14:52'),
(4, 'Luxury Retreat', 1000.00, 20.00, 800.00, '2024-12-31 08:14:52', '2024-12-31 08:14:52'),
(5, 'Family Vacation', 600.00, 12.00, 528.00, '2024-12-31 08:14:52', '2024-12-31 08:14:52'),
(6, 'q', 100.00, 10.00, 90.00, '2024-12-31 08:17:02', '2024-12-31 08:17:02'),
(7, 'Z', 11.00, 1.00, 10.89, '2024-12-31 12:48:58', '2024-12-31 12:48:58');

-- --------------------------------------------------------

--
-- Table structure for table `package_bookings`
--

CREATE TABLE `package_bookings` (
  `booking_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `package_id` int(11) NOT NULL,
  `payment_method` enum('Credit Card','Cash','Bank Transfer') NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `currency` enum('USD','TK') NOT NULL,
  `status` enum('Confirmed','Cancelled') NOT NULL DEFAULT 'Confirmed',
  `booking_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `package_bookings`
--

INSERT INTO `package_bookings` (`booking_id`, `user_id`, `package_id`, `payment_method`, `amount`, `currency`, `status`, `booking_date`) VALUES
(8, 1, 6, 'Cash', 9900.00, 'TK', 'Confirmed', '2024-12-31 12:22:26');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `room_number` int(11) NOT NULL,
  `room_size` varchar(50) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `availability` enum('available','booked') NOT NULL,
  `offer_price` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`room_number`, `room_size`, `price`, `availability`, `offer_price`, `created_at`, `updated_at`) VALUES
(1, 'Small', 100.00, 'available', 80.00, '2024-12-31 09:12:27', '2024-12-31 09:12:27'),
(2, 'Medium', 150.00, 'available', 120.00, '2024-12-31 09:12:27', '2024-12-31 09:12:27'),
(3, 'Large', 200.00, '', NULL, '2024-12-31 09:12:27', '2024-12-31 09:12:27'),
(4, 'Medium', 180.00, 'available', 100.00, '2024-12-31 09:12:27', '2024-12-31 12:05:14'),
(5, 'Small', 120.00, 'available', 100.00, '2024-12-31 09:12:27', '2024-12-31 12:54:41'),
(6, 's', 111.00, 'booked', NULL, '2024-12-31 12:08:56', '2024-12-31 12:10:15'),
(7, 'd', 122.00, 'booked', NULL, '2024-12-31 12:09:11', '2024-12-31 12:09:11'),
(8, 'Z', 11.00, 'available', 1.00, '2024-12-31 12:48:46', '2024-12-31 12:54:44');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `role` enum('user','admin') DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `email`, `phone`, `role`, `created_at`) VALUES
(1, 's', 's12345@', 's@gmail.com', '01753177651', 'admin', '2024-12-31 08:16:04'),
(3, 'a', 'a12345@', 'a@gmail.com', '01863732789', 'user', '2024-12-31 08:21:58');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `room_number` (`room_number`);

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`employee_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- Indexes for table `extra_services`
--
ALTER TABLE `extra_services`
  ADD PRIMARY KEY (`service_id`);

--
-- Indexes for table `extra_service_bookings`
--
ALTER TABLE `extra_service_bookings`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `service_id` (`service_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `hotel_policy`
--
ALTER TABLE `hotel_policy`
  ADD PRIMARY KEY (`policy_id`);

--
-- Indexes for table `packages`
--
ALTER TABLE `packages`
  ADD PRIMARY KEY (`package_id`);

--
-- Indexes for table `package_bookings`
--
ALTER TABLE `package_bookings`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `package_id` (`package_id`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`room_number`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `employees`
--
ALTER TABLE `employees`
  MODIFY `employee_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `extra_services`
--
ALTER TABLE `extra_services`
  MODIFY `service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `extra_service_bookings`
--
ALTER TABLE `extra_service_bookings`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `packages`
--
ALTER TABLE `packages`
  MODIFY `package_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `package_bookings`
--
ALTER TABLE `package_bookings`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `room_number` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`room_number`) REFERENCES `rooms` (`room_number`) ON DELETE CASCADE;

--
-- Constraints for table `extra_service_bookings`
--
ALTER TABLE `extra_service_bookings`
  ADD CONSTRAINT `extra_service_bookings_ibfk_1` FOREIGN KEY (`service_id`) REFERENCES `extra_services` (`service_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `extra_service_bookings_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `package_bookings`
--
ALTER TABLE `package_bookings`
  ADD CONSTRAINT `package_bookings_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `packages` (`package_id`) ON DELETE CASCADE;


--
-- Metadata
--
USE `phpmyadmin`;

--
-- Metadata for table bookings
--

--
-- Metadata for table employees
--

--
-- Metadata for table extra_services
--

--
-- Metadata for table extra_service_bookings
--

--
-- Metadata for table hotel_policy
--

--
-- Metadata for table packages
--

--
-- Metadata for table package_bookings
--

--
-- Metadata for table rooms
--

--
-- Dumping data for table `pma__table_uiprefs`
--

INSERT INTO `pma__table_uiprefs` (`username`, `db_name`, `table_name`, `prefs`, `last_update`) VALUES
('root', 'sdp_200', 'rooms', '{\"sorted_col\":\"`rooms`.`offer_price` DESC\",\"CREATE_TIME\":\"2024-12-31 15:11:59\",\"col_order\":[0,1,2,4,3,5,6],\"col_visib\":[1,1,1,1,1,1,1]}', '2024-12-31 11:24:32');

--
-- Metadata for table users
--

--
-- Metadata for database sdp_200
--
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
