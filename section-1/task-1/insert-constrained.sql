-- Lessons for 'Data Science 101' (course_id = 6)
INSERT INTO Lessons (course_id, lesson_name, lesson_description, video_url, video_duration) 
VALUES 
(6, 'Lesson 1: What is Data Science?', 'Introduction to Data Science', 'https://example.com/ds_intro', INTERVAL '1:20:00'),
(6, 'Lesson 2: Machine Learning Basics', 'Learn the basics of machine learning', 'https://example.com/ml_basics', INTERVAL '1:10:00'),
(6, 'Lesson 3: Introduction to Python for Data Science', 'Learn Python for data analysis', 'https://example.com/python_ds', INTERVAL '2:00:00');

-- Lessons for 'Algorithms and Data Structures' (course_id = 7)
INSERT INTO Lessons (course_id, lesson_name, lesson_description, video_url, video_duration) 
VALUES 
(7, 'Lesson 1: Sorting Algorithms', 'Learn different sorting algorithms', 'https://example.com/sorting_algorithms', INTERVAL '1:30:00'),
(7, 'Lesson 2: Binary Trees', 'Introduction to binary trees', 'https://example.com/binary_trees', INTERVAL '1:50:00'),
(7, 'Lesson 3: Graph Algorithms', 'Introduction to graph algorithms', 'https://example.com/graph_algorithms', INTERVAL '1:45:00');

-- Lessons for 'Mobile Application Development' (course_id = 8)
INSERT INTO Lessons (course_id, lesson_name, lesson_description, video_url, video_duration) 
VALUES 
(8, 'Lesson 1: Introduction to Flutter', 'Building mobile apps with Flutter', 'https://example.com/flutter_intro', INTERVAL '1:00:00'),
(8, 'Lesson 2: Designing User Interfaces', 'Learn how to design UI for mobile apps', 'https://example.com/ui_design', INTERVAL '1:20:00');

-- Lessons for 'Quantum Computing' (course_id = 9)
INSERT INTO Lessons (course_id, lesson_name, lesson_description, video_url, video_duration) 
VALUES 
(9, 'Lesson 1: What is Quantum Computing?', 'Basics of quantum computing', 'https://example.com/qc_intro', INTERVAL '2:15:00'),
(9, 'Lesson 2: Qubits and Quantum Gates', 'Introduction to qubits and quantum gates', 'https://example.com/qubits_gates', INTERVAL '1:45:00');

-- Lessons for 'Cyber Security Fundamentals' (course_id = 10)
INSERT INTO Lessons (course_id, lesson_name, lesson_description, video_url, video_duration) 
VALUES 
(10, 'Lesson 1: Cyber Security Basics', 'Introduction to cyber security', 'https://example.com/cs_basics', INTERVAL '1:30:00'),
(10, 'Lesson 2: Network Security', 'Learn how to secure networks', 'https://example.com/network_security', INTERVAL '1:40:00');

-- Lessons for 'Artificial Intelligence' (course_id = 11)
INSERT INTO Lessons (course_id, lesson_name, lesson_description, video_url, video_duration) 
VALUES 
(11, 'Lesson 1: Neural Networks', 'Introduction to neural networks', 'https://example.com/neural_networks', INTERVAL '1:50:00'),
(11, 'Lesson 2: Deep Learning Basics', 'Basics of deep learning', 'https://example.com/deep_learning', INTERVAL '2:00:00');

-- Lessons for 'Blockchain Technology' (course_id = 12)
INSERT INTO Lessons (course_id, lesson_name, lesson_description, video_url, video_duration) 
VALUES 
(12, 'Lesson 1: Blockchain Basics', 'Introduction to blockchain technology', 'https://example.com/blockchain_basics', INTERVAL '1:30:00'),
(12, 'Lesson 2: Smart Contracts', 'Learn about smart contracts', 'https://example.com/smart_contracts', INTERVAL '1:20:00');

-- Enroll students in 'Data Science 101'
INSERT INTO Enrollments (user_id, course_id, enroll_date) 
VALUES 
(10, 6, '2024-01-01'),  -- Sarah Connor is enrolled
(11, 6, '2024-01-02'),  -- Tom Holland is enrolled
(12, 6, '2024-01-03');  -- Lara Croft is enrolled

-- Enroll students in 'Algorithms and Data Structures'
INSERT INTO Enrollments (user_id, course_id, enroll_date) 
VALUES 
(13, 7, '2024-01-05'),  -- Bruce Wayne is enrolled
(14, 7, '2024-01-06'),  -- Clark Kent is enrolled
(15, 7, '2024-01-07');  -- Diana Prince is enrolled

-- Enroll students in 'Mobile Application Development'
INSERT INTO Enrollments (user_id, course_id, enroll_date) 
VALUES 
(16, 8, '2024-01-08'),  -- Peter Parker is enrolled
(17, 8, '2024-01-09');  -- Tony Stark is enrolled

-- Assign teachers to 'Data Science 101'
INSERT INTO TeacherAssignments (user_id, course_id, assignment_date) 
VALUES 
(18, 6, '2024-01-01');  -- Prof. X is teaching Data Science

-- Assign teachers to 'Algorithms and Data Structures'
INSERT INTO TeacherAssignments (user_id, course_id, assignment_date) 
VALUES 
(19, 7, '2024-01-02');  -- Dr. Strange is teaching Algorithms

-- Assign teachers to 'Mobile Application Development'
INSERT INTO TeacherAssignments (user_id, course_id, assignment_date) 
VALUES 
(20, 8, '2024-01-03');  -- Ms. Marvel is teaching Mobile Development

-- Sarah Connor completes Lesson 1 of 'Data Science 101' (lesson_id = 9)
INSERT INTO LessonCompletion (user_id, lesson_id, completion_status, completion_date, watched_duration) 
VALUES 
(10, 9, TRUE, '2024-01-10', INTERVAL '1:20:00');  -- Sarah completed the lesson

-- Tom Holland watches part of Lesson 2 of 'Data Science 101' (lesson_id = 10)
INSERT INTO LessonCompletion (user_id, lesson_id, completion_status, completion_date, watched_duration) 
VALUES 
(11, 10, FALSE, '2024-01-11', INTERVAL '0:50:00');  -- Tom watched 50 minutes, did not complete

-- Bruce Wayne completes Lesson 1 of 'Algorithms and Data Structures' (lesson_id = 13)
INSERT INTO LessonCompletion (user_id, lesson_id, completion_status, completion_date, watched_duration) 
VALUES 
(13, 13, TRUE, '2024-01-12', INTERVAL '1:30:00');  -- Bruce completed the lesson

-- Clark Kent watches part of Lesson 2 of 'Algorithms and Data Structures' (lesson_id = 14)
INSERT INTO LessonCompletion (user_id, lesson_id, completion_status, completion_date, watched_duration) 
VALUES 
(14, 14, FALSE, '2024-01-13', INTERVAL '1:20:00');  -- Clark watched 1 hour 20 minutes, did not complete

-- Peter Parker completes Lesson 1 of 'Mobile Application Development' (lesson_id = 17)
INSERT INTO LessonCompletion (user_id, lesson_id, completion_status, completion_date, watched_duration) 
VALUES 
(16, 17, TRUE, '2024-01-14', INTERVAL '1:00:00');  -- Peter completed the lesson

-- Tony Stark watches part of Lesson 2 of 'Mobile Application Development' (lesson_id = 18)
INSERT INTO LessonCompletion (user_id, lesson_id, completion_status, completion_date, watched_duration) 
VALUES 
(17, 18, FALSE, '2024-01-15', INTERVAL '0:45:00');  -- Tony watched 45 minutes, did not complete