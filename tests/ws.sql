-- make sure there is user 1 and init resources
insert into projects (project_id, title, description, status, creation_date, owner_id, resource_id) values (1, 'Test Project', 'just a test project', 'open', '2024-04-02 13:17:35.374492+01', 1, 1);
insert into sessions (session_id, project_id, title, ideation_technique, start_time, session_status, round_time, nb_rounds) values (1, 1, 'first session', 'brain_writing', '2024-04-02 13:17:35.374492+01', 'open', 5, 1);
insert into project_user (project_id, user_id, role, invitation_status, invitation_time) values (1, 1, 'Admin', 'accepted', '2024-04-02 13:17:35.374492+01');

-- password: hehe
insert into users (name, esi_email, profile_picture, last_activity, hash_password) values ('Potato chip', 'mc_chip@esi.dz', 'https://www.esi.dz/edt.html', '2024-04-02 13:17:35.374492+01','$2b$12$D2UN50rgSjLOL.P9EQF1seOZng1CUlFxqI5aP04XK4k4n.FIWSkhu');
insert into project_user (project_id, user_id, role, invitation_status, invitation_time) values (1, 2, 'user', 'accepted', '2024-04-02 13:17:35.374492+01');
