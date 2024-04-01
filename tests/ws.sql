insert into projects (title, description, status, owner_id, resource_id) values ('Test Project', 'just a test project', 'open', 1, 1);
insert into sessions (project_id, title, ideation_technique, session_status) values (2, 'first session', 'brain-wrting', 'open');
insert into project_user (project_id, user_id, role, invitation_status) values (2, 1, 'moderator', 'accepted');

-- password: hehe
insert into users (name, esi_email, profile_picture, hash_passoword) values ('Potato chip', 'mc_chip@esi.dz', 'https://www.esi.dz/edt.html', '$2b$12$D2UN50rgSjLOL.P9EQF1seOZng1CUlFxqI5aP04XK4k4n.FIWSkhu');
insert into project_user (project_id, user_id, role, invitation_status) values (2, 2, 'user', 'accepted');
