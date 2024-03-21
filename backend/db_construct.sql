CREATE TABLE users (
	uid VARCHAR(255),
	is_teacher BOOLEAN,
	is_admin BOOLEAN,
	PRIMARY KEY(uid)
);

CREATE TABLE courses (
	course_id INT GENERATED ALWAYS AS IDENTITY, 
	name VARCHAR(50) NOT NULL,
	ufora_id VARCHAR(50),
	teacher VARCHAR(255) NOT NULL,
	CONSTRAINT fk_teacher FOREIGN KEY(teacher) REFERENCES users(uid) ON DELETE CASCADE,
	PRIMARY KEY(course_id)
);

CREATE TABLE course_join_codes (
    join_code UUID DEFAULT gen_random_uuid() NOT NULL,
    course_id INT NOT NULL,
	expiry_time DATE,
	for_admins BOOLEAN NOT NULL,
	CONSTRAINT fk_course_join_link FOREIGN KEY(course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
	PRIMARY KEY(join_code)
);

CREATE TABLE course_admins (
	course_id INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
	uid VARCHAR(255) NOT NULL REFERENCES users(uid) ON DELETE CASCADE,
	PRIMARY KEY(course_id, uid)
);

CREATE TABLE course_students (
	course_id INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
	uid VARCHAR(255) NOT NULL REFERENCES users(uid) ON DELETE CASCADE,
	PRIMARY KEY(course_id, uid)
);

CREATE TABLE projects (
	project_id INT GENERATED ALWAYS AS IDENTITY,
	title VARCHAR(50) NOT NULL,
	description TEXT NOT NULL,
	assignment_file VARCHAR(50),
	deadline TIMESTAMP WITH TIME ZONE,
	course_id INT NOT NULL,
	visible_for_students BOOLEAN NOT NULL,
	archived BOOLEAN NOT NULL,
	test_path VARCHAR(50),
	script_name VARCHAR(50),
	regex_expressions VARCHAR(50)[],
	PRIMARY KEY(project_id),
	CONSTRAINT fk_course FOREIGN KEY(course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

CREATE TABLE submissions (
	submission_id INT GENERATED ALWAYS AS IDENTITY,
	uid VARCHAR(255) NOT NULL,
	project_id INT NOT NULL,
	grading FLOAT CHECK (grading >= 0 AND grading <= 20),
	submission_time TIMESTAMP WITH TIME ZONE NOT NULL,
	submission_path VARCHAR(50) NOT NULL,
	submission_status BOOLEAN NOT NULL,
	PRIMARY KEY(submission_id),
	CONSTRAINT fk_project FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
	CONSTRAINT fk_user FOREIGN KEY(uid) REFERENCES users(uid) ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION remove_expired_codes()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM course_join_codes
    WHERE expiry_time < CURRENT_DATE;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER remove_expired_codes_trigger
AFTER INSERT OR UPDATE ON course_join_codes
FOR EACH ROW EXECUTE FUNCTION remove_expired_codes();
