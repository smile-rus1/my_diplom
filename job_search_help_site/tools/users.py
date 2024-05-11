class UsersTools:
    @staticmethod
    def check_user_role(user):
        if hasattr(user, 'company'):
            return "company"

        elif hasattr(user, 'applicant'):
            return "applicant"


