from mainapp.auth import GroupName

super_admin_user = {
    'username': 'superadmin',
    'password': 'superadmin',
    'email': 'superadmin@mail.com',
    'first_name': 'superadmin',
    'last_name': 'superadmin',
    'groups': GroupName.all_values(),
}


def get_dev_user_list() -> list[dict]:
    users = [super_admin_user]
    for group_name in GroupName.all_values():
        users.append(
            {
                'username': f'{group_name}_user',
                'email': f'{group_name}@mail.com',
                'password': group_name,
                'first_name': f'{group_name}_first_name',
                'last_name': f'{group_name}_last_name',
                'groups': [group_name],
            }
        )
    return users
