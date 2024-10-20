--Assumes Enrollements only tracks users who's role is a Student
--So there is no need to join the UserRoles and Roles table
SELECT u.user_id, u.name, u.email 
FROM Users u
JOIN Enrollments e ON u.user_id = e.user_id
WHERE e.course_id = 5