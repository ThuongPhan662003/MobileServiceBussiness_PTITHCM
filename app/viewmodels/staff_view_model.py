class StaffViewModel:
    def __init__(self, staff, role_name=None, username=None, password=None):
        self.id = staff.id
        self.full_name = staff.full_name
        self.card_id = staff.card_id
        self.phone = staff.phone
        self.email = staff.email
        self.is_active = staff.is_active
        self.gender = staff.gender
        self.birthday = staff.birthday
        self.account_id = staff.account_id
        self.role_name = role_name
        self.username = username 
        self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'card_id': self.card_id,
            'phone': self.phone,
            'email': self.email,
            'is_active': self.is_active,
            'gender': self.gender,
            'birthday': self.birthday,
            'account_id': self.account_id,
            'role_name': self.role_name,
            'username': self.username,
            'password': self.password
        }