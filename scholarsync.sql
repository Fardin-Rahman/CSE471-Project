-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Aug 14, 2023 at 08:41 PM
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
-- Database: `scholarsync`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(10) UNSIGNED NOT NULL,
  `course_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `course_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `course_name`, `course_code`, `image`, `price`) VALUES
(1, 'Introduction to Python Programming', 'PY101', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.sololearn.com%2Flearn%2Fcourses%2Fpython-introduction&psig=AOvVaw0yPCvAY3Cl0xTSjtKEVYo-&ust=1691954136573000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCOjY8MTq14ADFQAAAAAdAAAAABAI', 500),
(2, 'Web Development Fundamentals', 'WD200', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.b3net.com%2Funderstanding-the-fundamentals-of-website-development&psig=AOvVaw1WBkDfKr19W3V_o2bjxtDk&ust=1691972602369000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCMiM1Kqv2IADFQAAAAAdAAAAABAI', 600),
(3, 'Digital Marketing Essentials', 'DM301', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fbpicolor.com%2F10-ways-to-building-a-strong-online-presence-digital-marketing-essentials%2Fdigital-marketing-essentials-sm-share%2F&psig=AOvVaw20k9qXel1nTLTQHOS4ShSj&ust=1691972664642000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCLjhi8yv2IADFQAAAAAdAAAAABAJ', 550),
(4, 'Data Science Basics', 'DS401', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fcareerfoundry.com%2Fen%2Fblog%2Fdata-analytics%2Fdata-analytics-tools%2F&psig=AOvVaw0iV5_0z-BRvB23wGANMPkl&ust=1691972719587000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCOCX5-ev2IADFQAAAAAdAAAAABAL', 800),
(5, 'Graphic Design Fundamentals', 'GD502', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fjustcreative.com%2Ffundamentals-of-graphicdesign%2F&psig=AOvVaw39kGO2QDOqhZyY363y9U23&ust=1691972824740000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCLj98Zaw2IADFQAAAAAdAAAAABAD', 900);

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `serialno` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `basic_mode` tinyint(1) NOT NULL,
  `image` varchar(2555) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`serialno`, `name`, `email`, `password`, `basic_mode`, `image`) VALUES
(1, 'Jack', 'nothing@g.com', '121', 1, 'https://i.pinimg.com/1200x/34/27/05/34270507b49ed110d38b9bf327f80302.jpg'),
(27, 'new', 'fine@g.com', '404', 0, 'image2.jpeg'),
(32, 'test', 'something@gmail.com', '561', 1, 'image3.jpeg'),
(36, 'Juha', 'juha@gmail.com', '123', 0, 'https://c4.wallpaperflare.com/wallpaper/749/423/664/anime-girl-brunette-glasses-wallpaper-preview.jpg'),
(37, 'Alex', 'alex@yahoo.com', '101', 1, ''),
(38, 'Alex', 'b@gmail.com', '101', 1, ''),
(39, 'fardin', 'fardin@g.c', '1', 1, 'https://i.pinimg.com/736x/e6/d1/e0/e6d1e04fa8ed09e1b7a6ef3cd7fefa53.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `Job_Title` varchar(50) NOT NULL,
  `Company_Name` varchar(50) NOT NULL,
  `Requirement` varchar(50) NOT NULL,
  `Location` varchar(50) NOT NULL,
  `Job_Code` int(11) NOT NULL,
  `Deadline` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `jobs`
--

INSERT INTO `jobs` (`Job_Title`, `Company_Name`, `Requirement`, `Location`, `Job_Code`, `Deadline`) VALUES
('Senior Frontend Developer', 'AB Tech', '2 years experience', 'Banani, Dhaka', 1, '2023-11-17 23:06:17'),
('Junior Frontend Developer', 'IT Cell', '1 year job experience', 'Mohakhali, Dhaka', 2, '2023-10-05 23:07:22'),
('Node.Js Internship', 'High Tech', 'Bachelor or equivalent degree', 'Banani, Dhaka', 3, '2023-10-19 00:12:43'),
('Chief Financial Officer', 'One Direction Companies Limited', '8 years of experience ', 'Dhaka', 12, '2023-10-06 00:14:04'),
('General Manager (A & F)-Textile & RMG Division', 'Deshbandhu Group', '15 years of experience, M.Com in Accounting.', 'Dhanmondi, Dhaka', 13, '2023-09-08 00:14:04'),
('Ai Engineer', 'Google', 'Computer Science degree', 'Khulna', 14, '2023-09-08 00:19:49'),
('Product Manger', 'Pather', '2 years of experience in related field', 'Mirpur, Dhaka ', 15, '2023-09-09 00:19:49');

-- --------------------------------------------------------

--
-- Table structure for table `premium`
--

CREATE TABLE `premium` (
  `c_id` int(11) NOT NULL,
  `c_name` varchar(250) NOT NULL,
  `wishlist` enum('yes','no') NOT NULL DEFAULT 'no',
  `cart` enum('yes','no') NOT NULL DEFAULT 'no'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `premium`
--

INSERT INTO `premium` (`c_id`, `c_name`, `wishlist`, `cart`) VALUES
(1, 'Python for Beginners', 'no', 'no');

-- --------------------------------------------------------

--
-- Table structure for table `profcontacts`
--

CREATE TABLE `profcontacts` (
  `serial` int(11) NOT NULL,
  `FullName` text NOT NULL,
  `uniName` text NOT NULL,
  `designation` text NOT NULL,
  `mail` varchar(40) NOT NULL,
  `passw` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `profcontacts`
--

INSERT INTO `profcontacts` (`serial`, `FullName`, `uniName`, `designation`, `mail`, `passw`) VALUES
(1, 'Mr. xyz', 'Brac University', 'Assistant Professor ', 'xyz@email.com', '123'),
(2, 'Jem', 'University Of London', 'Senior Lecturer', 'jem@uol.com', '111');

-- --------------------------------------------------------

--
-- Table structure for table `prof_post`
--

CREATE TABLE `prof_post` (
  `id` int(20) NOT NULL,
  `name` text NOT NULL,
  `time` datetime NOT NULL DEFAULT current_timestamp(),
  `post` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `prof_post`
--

INSERT INTO `prof_post` (`id`, `name`, `time`, `post`) VALUES
(1, 'xyz', '2023-08-13 11:02:00', 'The International Max Planck Research School for Environmental, Cellular, and Molecular he IMPRS-Mic is a joint initiative of the Max Planck Institute for Terrestrial Microbiology and the Philipps-Universität Marburg. offer PhD projects in the following research areas:\r\n\r\n- Biochemistry and Structural Biology\r\n- Microbial Ecology and Interactions\r\n- Molecular and Cellular Microbiology\r\n- Microbial Genomics\r\n- Systems and Synthetic Microbiology\r\n\r\nLast date to apply 31 Jan 2023.\r\n\r\n'),
(5, 'Mr. xyz', '2023-08-13 05:41:12', 'Currently I am looking for few phd candidates for my upcoming research work. Requirements- ML, Ai, NLPs. For further info mail me. '),
(6, 'Mr. xyz', '2023-08-13 09:03:12', 'i ');

-- --------------------------------------------------------

--
-- Table structure for table `Query`
--

CREATE TABLE `Query` (
  `q_id` int(11) NOT NULL,
  `question` text NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `poster` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Query`
--

INSERT INTO `Query` (`q_id`, `question`, `date`, `poster`) VALUES
(1, 'What is NN?', '2023-08-10 20:41:26', 'Juha'),
(3, 'what is machine learning?', '2023-08-10 20:41:26', 'Alex'),
(18, 'Any update on Scholarships?', '2023-08-10 20:41:26', 'Alex\r\n');

-- --------------------------------------------------------

--
-- Table structure for table `Reply`
--

CREATE TABLE `Reply` (
  `r_id` int(11) NOT NULL,
  `answer` text NOT NULL,
  `time` datetime NOT NULL DEFAULT current_timestamp(),
  `ans_id` int(11) NOT NULL,
  `person` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Reply`
--

INSERT INTO `Reply` (`r_id`, `answer`, `time`, `ans_id`, `person`) VALUES
(1, 'NN is a model', '2023-07-29 10:58:16', 1, 'Alex'),
(1, 'Need to work on NN', '2023-07-29 10:58:31', 2, 'Test'),
(2, 'Use google !!!!', '2023-07-29 10:58:45', 3, 'Juha'),
(2, 'Math problem', '2023-07-29 12:04:12', 4, 'Juha'),
(3, 'Want to know too', '2023-07-29 08:55:27', 5, 'Alex'),
(19, 'I am interested tooo', '2023-07-29 10:43:37', 6, 'New'),
(19, 'Me too', '2023-07-29 10:43:51', 7, 'New'),
(16, 'It is kinda vector', '2023-07-29 10:44:45', 8, 'Alex'),
(19, 'Same', '2023-08-10 14:39:47', 12, 'Alex'),
(18, 'fine', '2023-08-13 05:22:18', 13, 'Juha');

-- --------------------------------------------------------

--
-- Table structure for table `scholarship`
--

CREATE TABLE `scholarship` (
  `sc_code` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `university` varchar(50) NOT NULL,
  `requirement` varchar(100) NOT NULL,
  `country` varchar(30) NOT NULL,
  `deadline` datetime NOT NULL,
  `link` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `scholarship`
--

INSERT INTO `scholarship` (`sc_code`, `name`, `university`, `requirement`, `country`, `deadline`, `link`) VALUES
(1, 'BRACU merit-based scholarship', 'BRAC University', '90% of grade in Bachelor Degree, IELTS 6', 'Bangladesh', '2023-11-04 00:47:04', 'https://www.bracu.ac.bd/'),
(2, 'BNU Asylum Seeker Scholarship', 'Bucks New University', 'Application Registration Card (ARC) or Asylum Seeker status (under-1951 UN Convention)', 'United Kingdom', '2023-09-23 00:59:35', 'https://www.bucks.ac.uk/');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`serialno`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD UNIQUE KEY `Job Code` (`Job_Code`);

--
-- Indexes for table `premium`
--
ALTER TABLE `premium`
  ADD PRIMARY KEY (`c_id`);

--
-- Indexes for table `profcontacts`
--
ALTER TABLE `profcontacts`
  ADD PRIMARY KEY (`serial`);

--
-- Indexes for table `prof_post`
--
ALTER TABLE `prof_post`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Query`
--
ALTER TABLE `Query`
  ADD PRIMARY KEY (`q_id`);

--
-- Indexes for table `Reply`
--
ALTER TABLE `Reply`
  ADD PRIMARY KEY (`ans_id`);

--
-- Indexes for table `scholarship`
--
ALTER TABLE `scholarship`
  ADD PRIMARY KEY (`sc_code`),
  ADD UNIQUE KEY `name` (`name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `serialno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `Job_Code` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `premium`
--
ALTER TABLE `premium`
  MODIFY `c_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `profcontacts`
--
ALTER TABLE `profcontacts`
  MODIFY `serial` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `prof_post`
--
ALTER TABLE `prof_post`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `Query`
--
ALTER TABLE `Query`
  MODIFY `q_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `Reply`
--
ALTER TABLE `Reply`
  MODIFY `ans_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `scholarship`
--
ALTER TABLE `scholarship`
  MODIFY `sc_code` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
