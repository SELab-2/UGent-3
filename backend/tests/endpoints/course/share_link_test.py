from project.models.courses import Course

class TestCourseShareLinkEndpoint:

    def test_get_share_links(self, db_with_course, client):
        """Test whether the share links are accesible"""
        example_course = db_with_course.query(Course).first()
        response = client.get(f"courses/{example_course.course_id}/join_codes")
        assert response.status_code == 200

    def test_post_share_links(self, db_with_course, client):
        """Test whether the share links are accesible to post to"""
        example_course = db_with_course.query(Course).first()
        response = client.post(f"courses/{example_course.course_id}/join_codes", json={"for_admins": True})
        assert response.status_code == 201
    
    def test_delete_share_links(self, share_code_admin, client):
        """Test whether the share links are accesible to delete"""
        response = client.delete(f"courses/{share_code_admin.course_id}/join_codes/{share_code_admin.join_code}")
        assert response.status_code == 200

    def test_get_share_links_404(self, client):
        """Test whether the share links are accesible"""
        response = client.get(f"courses/0/join_codes")
        assert response.status_code == 404

    def test_post_share_links_404(self, client):
        """Test whether the share links are accesible to post to"""
        response = client.post(f"courses/0/join_codes", json={"for_admins": True})
        assert response.status_code == 404

    def test_delete_share_links_404(self, client):
        """Test whether the share links are accesible to delete"""
        response = client.delete(f"courses/0/join_codes/0")
        assert response.status_code == 404
    
    def test_for_admins_required(self, db_with_course, client):
        """Test whether the for_admins field is required"""
        example_course = db_with_course.query(Course).first()
        response = client.post(f"courses/{example_course.course_id}/join_codes", json={})
        assert response.status_code == 400
