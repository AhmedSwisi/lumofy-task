WITH student_courses AS (
    SELECT u.user_id, u.name, c.course_id, c.course_name
    FROM Users u
    JOIN Enrollments e ON u.user_id = e.user_id
    JOIN Courses c ON e.course_id = c.course_id
    JOIN UserRoles ur ON u.user_id = ur.user_id
    JOIN Roles r ON ur.role_id = r.role_id
    WHERE r.role_name = 'Student'
),
lesson_stats AS (
    SELECT
        c.course_id,
        l.course_id AS lesson_course_id,
        l.lesson_id,
        COUNT(l.lesson_id) AS total_lessons,
        SUM(CASE WHEN lc.completion_status = TRUE THEN 1 ELSE 0 END) AS lessons_completed
    FROM Courses c
    JOIN Lessons l ON c.course_id = l.course_id
    LEFT JOIN LessonCompletion lc ON l.lesson_id = lc.lesson_id
    GROUP BY c.course_id, l.lesson_id
)
SELECT 
    sc.user_id,
    sc.name,
    sc.course_id,
    sc.course_name,
    COUNT(ls.lesson_id) AS total_lessons,
    SUM(ls.lessons_completed) AS lessons_completed,
    ROUND(
        (SUM(ls.lessons_completed) * 100.0 / COUNT(ls.lesson_id))
    ) AS progress_percentage
FROM student_courses sc
JOIN lesson_stats ls ON sc.course_id = ls.course_id
GROUP BY sc.user_id, sc.name, sc.course_id, sc.course_name
ORDER BY sc.user_id, sc.course_id;
