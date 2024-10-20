SELECT u.user_id, u.name, u.email, c.course_name, ta.course_id FROM Users u
JOIN TeacherAssignments ta ON u.user_id = ta.user_id
JOIN Courses c ON c.course_id = ta.course_id
WHERE u.user_id = 18;


