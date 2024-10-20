

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    date_of_birth DATE
);

-- Create Roles Table
CREATE TABLE Roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE UserRoles (
    user_role_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    role_id INT REFERENCES Roles(role_id) ON DELETE CASCADE,
    UNIQUE (user_id, role_id) -- Each user can have only one of each role
);

CREATE TABLE Courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE Lessons (
    lesson_id SERIAL PRIMARY KEY,
    course_id INT REFERENCES Courses(course_id) ON DELETE CASCADE,
    lesson_name VARCHAR(255) NOT NULL,
    lesson_description TEXT,
	video_url TEXT,
	video_duration INTERVAL HOUR TO SECOND
);

-- Create Enrollments Table (Students enrolling in courses)
CREATE TABLE Enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    course_id INT REFERENCES Courses(course_id) ON DELETE CASCADE,
    enroll_date DATE NOT NULL,
    UNIQUE (user_id, course_id)
);


CREATE TABLE TeacherAssignments (
    assignment_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    course_id INT REFERENCES Courses(course_id) ON DELETE CASCADE,
    assignment_date DATE NOT NULL,
    UNIQUE (user_id, course_id)
);

-- Create LessonCompletion Table (Tracking student progress)
CREATE TABLE LessonCompletion (
    completion_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    lesson_id INT REFERENCES Lessons(lesson_id) ON DELETE CASCADE,
    completion_status BOOLEAN NOT NULL DEFAULT FALSE,
    completion_date DATE,
	watched_duration INTERVAL HOUR TO SECOND,
    UNIQUE (user_id, lesson_id) -- A student can only complete a lesson once
);

