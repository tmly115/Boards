

class Profile_Edit_Form:
    def __init__(self, profile_edit_form_dict):
        self.profile_name = profile_edit_form_dict['profile_name']
        self.profile_bio = profile_edit_form_dict['profile_bio']
        self.profile_location = profile_edit_form_dict['profile_location']

class Create_Text_Post_Form:
    def __init__(self, create_post_form_dict):
        self.post_title = create_post_form_dict['title']
        self.post_content = create_post_form_dict['content']

class Create_Link_Post_Form:
    def __init__(self, create_post_form_dict):
        if self._validate(create_post_form_dict):
            self.post_title = create_post_form_dict['title']
            self.post_link = create_post_form_dict['link']
            self.error = False

    def _validate(self, create_post_form_dict):
        if 'https://' not in create_post_form_dict['link']:
            self.error = True
            self.error_description = 'Link used is not valid.'
        elif 'http://' in create_post_form_dict['link']:
            self.error = True
            self.error_description = 'Link used is not valid.'
        else:
            return True
