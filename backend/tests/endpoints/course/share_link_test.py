"""
This file contains the tests for the share link endpoints of the course resource.
"""

class TestCourseShareLinks:
    """
    Class that will respond to the /courses/course_id/students link
    teachers should be able to assign and remove students from courses,
    and everyone should be able to list all students assigned to a course
    """

    def test_get_share_links(self, valid_course_entry, client):
        """Test whether the share links are accessible"""
        response = client.get(f"courses/{valid_course_entry.course_id}/join_codes")
        assert response.status_code == 200

    def test_post_share_links(self, valid_course_entry, client):
        """Test whether the share links are accessible to post to"""
        response = client.post(
            f"courses/{valid_course_entry.course_id}/join_codes",
            json={"for_admins": True})
        assert response.status_code == 201

    def test_delete_share_links(self, share_code_admin, client):
        """Test whether the share links are accessible to delete"""
        response = client.delete(
            f"courses/{share_code_admin.course_id}/join_codes/{share_code_admin.join_code}")
        assert response.status_code == 200

    def test_get_share_links_404(self, client):
        """Test whether the share links are accessible"""
        response = client.get("courses/0/join_codes")
        assert response.status_code == 404

    def test_post_share_links_404(self, client):
        """Test whether the share links are accessible to post to"""
        response = client.post("courses/0/join_codes", json={"for_admins": True})
        assert response.status_code == 404

    def test_delete_share_links_404(self, client):
        """Test whether the share links are accessible to delete"""
        response = client.delete("courses/0/join_codes/0")
        assert response.status_code == 404

    def test_for_admins_required(self, valid_course_entry, client):
        """Test whether the for_admins field is required"""
        response = client.post(f"courses/{valid_course_entry.course_id}/join_codes", json={})
        assert response.status_code == 400
