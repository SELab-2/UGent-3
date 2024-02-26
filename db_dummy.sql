DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
	uid VARCHAR(255),
	is_teacher BOOLEAN,
	is_admin BOOLEAN,
	PRIMARY KEY(uid)
);

DROP TABLE IF EXISTS courses CASCADE;
CREATE TABLE courses (
	course_id INT GENERATED ALWAYS AS IDENTITY, 
	name VARCHAR(50) NOT NULL,
	ufora_id VARCHAR(50),
	teacher VARCHAR(255) NOT NULL,
	CONSTRAINT fk_teacher FOREIGN KEY(teacher) REFERENCES users(uid),
	PRIMARY KEY(course_id)
);


DROP TABLE IF EXISTS course_admins CASCADE;
CREATE TABLE course_admins (
	course_id INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
	uid VARCHAR(255) NOT NULL REFERENCES users(uid) ON DELETE CASCADE,
	PRIMARY KEY(course_id, uid)
);

DROP TABLE IF EXISTS course_students CASCADE;
CREATE TABLE course_students (
	course_id INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
	uid VARCHAR(255) NOT NULL REFERENCES users(uid) ON DELETE CASCADE,
	PRIMARY KEY(course_id, uid)
);

DROP TABLE IF EXISTS projects CASCADE;
CREATE TABLE projects (
	project_id INT GENERATED ALWAYS AS IDENTITY,
	title VARCHAR(50) NOT NULL,
	descriptions TEXT NOT NULL,
	assignment_file VARCHAR(50),
	deadline TIMESTAMP WITH TIME ZONE,
	course_id INT NOT NULL,
	visible_for_students BOOLEAN NOT NULL,
	archieved BOOLEAN NOT NULL,
	test_path VARCHAR(50),
	script_name VARCHAR(50),
	regex_expressions VARCHAR(50)[],
	PRIMARY KEY(project_id),
	CONSTRAINT fk_course FOREIGN KEY(course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS submissions CASCADE;
CREATE TABLE submissions (
	submission_id INT GENERATED ALWAYS AS IDENTITY,
	uid VARCHAR(255) NOT NULL,
	project_id INT NOT NULL,
	grading INTEGER CHECK (grading >= 0 AND grading <= 20),
	submission_time TIMESTAMP WITH TIME ZONE NOT NULL,
	submission_path VARCHAR(50) NOT NULL,
	submission_status BOOLEAN NOT NULL,
	PRIMARY KEY(submission_id),
	CONSTRAINT fk_project FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
	CONSTRAINT fk_user FOREIGN KEY(uid) REFERENCES users(uid)
);


-- Insert dummy users
INSERT INTO users (uid, is_teacher, is_admin) VALUES
('user1', TRUE, TRUE),
('user2', TRUE, TRUE),
('user3', FALSE, FALSE),
('user4', FALSE, FALSE);

-- Insert dummy courses
INSERT INTO courses (name, ufora_id, teacher) VALUES
('Course 1', 'ufora123', 'user1'),
('Course 2', 'ufora456', 'user2');

-- Insert dummy course admins
INSERT INTO course_admins (course_id, uid) VALUES
(1, 'user1'),
(2, 'user2');

-- Insert dummy course students
INSERT INTO course_students (course_id, uid) VALUES
(1, 'user4'),
(2, 'user3');

-- Insert dummy projects
INSERT INTO projects (title, descriptions, assignment_file, deadline, course_id, visible_for_students, archieved, test_path, script_name, regex_expressions) VALUES
('Project 1', 'Description for Project 1', 'assignment1.pdf', '2024-03-01 00:00:00+00', 1, TRUE, FALSE, '/tests/test1.py', 'script1.py', ARRAY['expression1', 'expression2']),
('Project 2', 'Description for Project 2', 'assignment2.pdf', '2024-03-15 00:00:00+00', 2, TRUE, FALSE, '/tests/test2.py', 'script2.py', ARRAY['expression3', 'expression4']);

-- Insert dummy submissions
INSERT INTO submissions (uid, project_id, grading, submission_time, submission_path, submission_status) VALUES
('user4', 1, 15, '2024-02-20 08:00:00+00', '/submissions/submission1.zip', TRUE),
('user3', 2, 18, '2024-02-22 10:00:00+00', '/submissions/submission2.zip', TRUE);

