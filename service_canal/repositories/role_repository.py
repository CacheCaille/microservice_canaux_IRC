from app import db

def get_user_roles(channel_name, user_pseudo):
    """
    Retrieve user roles in a specific channel.
    """
    role = Role.query.filter_by(
        fk_user_name=user_name,
        fk_canal_name=canal_name
    ).first()
    if not canal:
        raise Exception(f"Channel {channel_name} not found")
    # only one role per user in a channel
    
    return role

def insert_user(pseudo, channel_name, role="INVITE", banned_reason=None):
    """
    Insert a user into a channel with a specific role.
    """
    new_role = Role(
        fk_user_name=pseudo,
        fk_canal_name=channel_name,
        role=role,
        banned_reason=banned_reason
    )
    db.session.add(new_role)
    db.session.commit()
    return new_role


