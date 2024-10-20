-- Inserting Students
INSERT INTO Users (name, email, date_of_birth) 
VALUES 
('John Doe', 'john@example.com', '2000-05-15'),
('Jane Smith', 'jane@example.com', '1999-03-22'),
('Alice Johnson', 'alice@example.com', '2001-02-10'),
('Bob Marley', 'bob@example.com', '2002-07-19'),
('Clara Wells', 'clara@example.com', '1998-11-05'),
('Sarah Connor', 'sarah.connor@example.com', '2000-01-15'),
('Tom Holland', 'tom.holland@example.com', '2001-04-10'),
('Lara Croft', 'lara.croft@example.com', '1999-09-18'),
('Bruce Wayne', 'bruce.wayne@example.com', '2002-11-25'),
('Clark Kent', 'clark.kent@example.com', '2000-07-22'),
('Diana Prince', 'diana.prince@example.com', '1998-06-01'),
('Peter Parker', 'peter.parker@example.com', '2001-08-09'),
('Tony Stark', 'tony.stark@example.com', '1999-12-29');

-- Inserting Teachers
INSERT INTO Users (name, email, date_of_birth) 
VALUES 
('Mr. Thompson', 'thompson@example.com', '1980-09-12'),
('Ms. Emily', 'emily@example.com', '1985-07-07'),
('Prof. X', 'prof.x@example.com', '1975-03-19'),
('Dr. Strange', 'strange@example.com', '1980-08-10'),
('Ms. Marvel', 'ms.marvel@example.com', '1985-11-05'),
('Wonder Woman', 'wonder.woman@example.com', '1978-02-28'),
('Batman', 'batman@example.com', '1972-05-15'),
('Superman', 'superman@example.com', '1974-07-04');

INSERT INTO Roles (role_name) 
VALUES 
('Student'),
('Teacher');

-- Assigning roles (Student role = 1, Teacher role = 2)
-- Assign Students
INSERT INTO UserRoles (user_id, role_id) 
VALUES 
(1, 1),  -- John Doe is a student
(2, 1),  -- Jane Smith is a student
(3, 1),  -- Alice Johnson is a student
(4, 1),  -- Bob Marley is a student
(5, 1),  -- Clara Wells is a student
(6, 1),  -- Sarah Connor is a student
(7, 1),  -- Tom Holland is a student
(8, 1),  -- Lara Croft is a student
(9, 1),  -- Bruce Wayne is a student
(10, 1), -- Clark Kent is a student
(11, 1), -- Diana Prince is a student
(12, 1), -- Peter Parker is a student
(13, 1); -- Tony Stark is a student

-- Assign Teachers
INSERT INTO UserRoles (user_id, role_id) 
VALUES 
(14, 2),  -- Mr. Thompson is a teacher
(15, 2),  -- Ms. Emily is a teacher
(16, 2),  -- Prof. X is a teacher
(17, 2),  -- Dr. Strange is a teacher
(18, 2),  -- Ms. Marvel is a teacher
(19, 2),  -- Wonder Woman is a teacher
(20, 2),  -- Batman is a teacher
(21, 2);  -- Superman is a teacher

INSERT INTO Courses (course_name, description) 
VALUES 
('Introduction to SQL', 'A beginner-level course on SQL'),
('Advanced Python', 'An advanced-level course on Python programming'),
('Introduction to Databases', 'Learn the basics of databases and SQL'),
('Machine Learning Fundamentals', 'Introduction to basic machine learning algorithms'),
('Web Development with JavaScript', 'Learn how to build dynamic websites using JavaScript'),
('Data Science 101', 'Introduction to Data Science and Machine Learning'),
('Algorithms and Data Structures', 'Advanced course on algorithms and data structures'),
('Mobile Application Development', 'Developing mobile applications using Flutter'),
('Quantum Computing', 'Introduction to the basics of Quantum Computing'),
('Cyber Security Fundamentals', 'Learn the fundamentals of cyber security'),
('Artificial Intelligence', 'Overview of AI concepts, including neural networks and deep learning'),
('Blockchain Technology', 'Introduction to blockchain and its applications');

-- Lessons for 'Introduction to SQL' (course_id = 1)
INSERT INTO Lessons (course_id, lesson_name, lesson_description, video_url, video_duration) 
VALUES 
(1, 'Lesson 1: SQL Basics', 'Introduction to SQL queries', 'https://example.com/sql_basics', INTERVAL '0:45:30'),
(1, 'Lesson 2: Advanced Queries', 'Learn advanced SQL techniques', 'https://example.com/advanced_sql', INTERVAL '1:20:00');

-- Lessons for 'Advanced Python' (course_id = 2)
INSERT INTO Lessons (course_id, lesson_name, lesson_description, video_url, video_duration) 
VALUES 
(2, 'Lesson 1: Python OOP', 'Introduction to object-oriented programming in Python', 'https://example.com/python_oop', INTERVAL '1:15:00'),
(2, 'Lesson 2: Python Metaprogramming', 'Learn metaprogramming in Python', 'https://example.com/metaprogramming', INTERVAL '1:30:00');

-- Lessons for 'Introduction to Databases' (course_id = 3)
INSERT INTO Lessons (course_id, lesson_name, lesson_description, video_url, video_duration) 
VALUES 
(3, 'Lesson 1: What is a Database?', 'Introduction to databases', 'https://example.com/db_intro', INTERVAL '1:10:00'),
(3, 'Lesson 2: SQL Basics', 'Learn SQL basics', 'https://example.com/sql_basics_db', INTERVAL '1:05:00');

-- Lessons for 'Machine Learning Fundamentals' (course_id = 4)
INSERT INTO Lessons (course_id, lesson_name, lesson_description, video_url, video_duration) 
VALUES 
(4, 'Lesson 1: Introduction to ML', 'Overview of machine learning', 'https://example.com/ml_intro', INTERVAL '0:50:00'),
(4, 'Lesson 2: Supervised Learning', 'Introduction to supervised learning', 'https://example.com/supervised_learning', INTERVAL '1:30:00');

-- Lessons for 'Web Development with JavaScript' (course_id = 5)
INSERT INTO Lessons (course_id, lesson_name, lesson_description, video_url, video_duration) 
VALUES 
(5, 'Lesson 1: JavaScript Basics', 'Learn the basics of JavaScript', 'https://example.com/js_basics', INTERVAL '1:00:00'),
(5, 'Lesson 2: DOM Manipulation', 'How to manipulate the DOM with JavaScript', 'https://example.com/dom_manipulation', INTERVAL '1:15:00');

-- Enroll students in 'Introduction to SQL'
INSERT INTO Enrollments (user_id, course_id, enroll_date) 
VALUES 
(1, 1, '2024-01-01'),  -- John Doe is enrolled
(2, 1, '2024-01-02');  -- Jane Smith is enrolled

-- Enroll students in 'Advanced Python'
INSERT INTO Enrollments (user_id, course_id, enroll_date) 
VALUES 
(3, 2, '2024-01-03'),  -- Alice Johnson is enrolled
(4, 2, '2024-01-04');  -- Bob Marley is enrolled

-- Enroll students in 'Introduction to Databases'
INSERT INTO Enrollments (user_id, course_id, enroll_date) 
VALUES 
(5, 3, '2024-01-05'),  -- Clara Wells is enrolled
(6, 3, '2024-01-06');  -- Sarah Connor is enrolled

-- Enroll students in 'Machine Learning Fundamentals'
INSERT INTO Enrollments (user_id, course_id, enroll_date) 
VALUES 
(7, 4, '2024-01-07'),  -- Tom Holland is enrolled
(8, 4, '2024-01-08');  -- Lara Croft is enrolled

-- Enroll students in 'Web Development with JavaScript'
INSERT INTO Enrollments (user_id, course_id, enroll_date) 
VALUES 
(9, 5, '2024-01-09'),  -- Bruce Wayne is enrolled
(10, 5, '2024-01-10'); -- Clark Kent is enrolled

-- Assign teachers to 'Introduction to SQL'
INSERT INTO TeacherAssignments (user_id, course_id, assignment_date) 
VALUES 
(14, 1, '2024-01-01');  -- Mr. Thompson is assigned

INSERT INTO TeacherAssignments (user_id, course_id, assignment_date) 
VALUES 
(15, 2, '2024-01-02');  -- Ms. Emily is assigned

-- Assign teachers to 'Introduction to Databases'
INSERT INTO TeacherAssignments (user_id, course_id, assignment_date) 
VALUES 
(16, 3, '2024-01-03');  -- Prof. X is assigned

-- Assign teachers to 'Machine Learning Fundamentals'
INSERT INTO TeacherAssignments (user_id, course_id, assignment_date) 
VALUES 
(17, 4, '2024-01-04');  -- Dr. Strange is assigned

-- Assign teachers to 'Web Development with JavaScript'
INSERT INTO TeacherAssignments (user_id, course_id, assignment_date) 
VALUES 
(18, 5, '2024-01-05');  -- Ms. Marvel is assigned

-- John Doe completes Lesson 1 of 'Introduction to SQL' (lesson_id = 1)
INSERT INTO LessonCompletion (user_id, lesson_id, completion_status, completion_date, watched_duration) 
VALUES 
(1, 1, TRUE, '2024-01-10', INTERVAL '0:45:30');  -- John completed the lesson

-- Jane Smith watches part of Lesson 2 of 'Introduction to SQL' (lesson_id = 2)
INSERT INTO LessonCompletion (user_id, lesson_id, completion_status, completion_date, watched_duration) 
VALUES 
(2, 2, FALSE, '2024-01-11', INTERVAL '1:00:00');  -- Jane watched 1 hour but didn’t complete
