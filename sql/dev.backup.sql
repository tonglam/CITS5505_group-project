-- User

INSERT INTO user (id, username, email, password_hash, avatar_url, use_google, use_github, security_question, security_answer, status, create_at, update_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'tonglam', 'bluedragon00000@gmail.com', '$2b$12$R49DZkkWelMYoCv2.mCQeemIVKkCNrzuA3Vekq6PxMpIk4jqjJbmW', 'https://avatars.githubusercontent.com/u/19681829?v=4', 1, 1, 'What is your favorite color?', 'blue', 'ACTIVE', '2024-04-21 14:36:18.896100', '2024-04-21 15:31:20.425434');
INSERT INTO user (id, username, email, password_hash, avatar_url, use_google, use_github, security_question, security_answer, status, create_at, update_at) VALUES ('b4ef71f8-409f-485f-b797-b44b5853a1f5', 'tonglan', 'qitonglan@gmail.com', '$2b$12$D7uO.K4xHTA62nmLd/WM4ODTeAU2tP/aGVFQf9o7HpdfKNdryF2Oi', 'https://www.gravatar.com/avatar/4ad8c50f623b6eccf0299d12005d39e7b670ac7e49654ee662016ba1c1915b54', 0, 0, 'Which color?', 'blue', 'ACTIVE', '2024-05-02 11:50:58.257018', '2024-05-02 11:50:58.257040');
INSERT INTO user (id, username, email, password_hash, avatar_url, use_google, use_github, security_question, security_answer, status, create_at, update_at) VALUES ('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 'Hayeensss', null, null, 'https://avatars.githubusercontent.com/u/145556077?v=4', 0, 1, '', '', 'ACTIVE', '2024-05-07 11:35:01.583653', '2024-05-07 11:35:01.583673');


-- User Preference

INSERT INTO user_preference (user_id, communities, interests, update_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', '[1, 3, 5, 7, 9]', '[1, 3, 5, 7]', '2024-04-22 05:36:18.811157');

-- User Record

INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 1, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 2, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 3, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 4, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 5, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 6, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 7, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 8, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 9, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 10, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 4, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 3, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 1, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 2, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 1, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 8, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 9, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 8, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 8, '2024-04-22 05:23:36.740414');
INSERT INTO user_record (user_id, request_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 10, '2024-04-22 05:23:36.740414');

-- User Like

INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 1, 2, '2024-05-03 09:30:00');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 2, 1, '2024-05-03 10:00:00');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 3, 4, '2024-05-03 11:30:00');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 4, 6, '2024-05-03 13:00:00');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 5, 6, '2024-05-03 14:30:00');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 6, 2, '2024-04-22 05:23:36.740414');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 7, 1, '2024-04-22 05:23:36.740414');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 8, 3, '2024-04-22 05:23:36.740414');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 9, 6, '2024-04-22 05:23:36.740414');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 10, 10, '2024-04-22 05:23:36.740414');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 12, 14, '2024-04-22 05:23:36.740414');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 14, 20, '2024-04-22 05:23:36.740414');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 16, 14, '2024-04-22 05:23:36.740414');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 18, 14, '2024-04-22 05:23:36.740414');
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 20, 1, '2024-04-22 05:23:36.740414');

-- User Save

INSERT INTO user_save (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 1, 1, '2024-04-22 05:23:36.740414');
INSERT INTO user_save (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 2, 4, '2024-04-22 05:23:36.740414');
INSERT INTO user_save (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 3, 4, '2024-04-22 05:23:36.740414');
INSERT INTO user_save (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 8, 10, '2024-04-22 05:23:36.740414');
INSERT INTO user_save (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 10, 6, '2024-04-22 05:23:36.740414');
INSERT INTO user_save (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 11, 8, '2024-04-22 05:23:36.740414');
INSERT INTO user_save (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 15, 2, '2024-04-22 05:23:36.740414');
INSERT INTO user_save (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 17, 2, '2024-04-22 05:23:36.740414');
INSERT INTO user_save (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 19, 10, '2024-04-22 05:23:36.740414');
INSERT INTO user_save (user_id, request_id, reply_id, create_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 20, 1, '2024-04-22 05:23:36.740414');

-- Community

INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Cinema Club', 1, 'A community for movie enthusiasts to discuss the latest films, classic cinema, and film industry trends.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('All Sports Forum', 2, 'Whether you''re into football, basketball, or swimming, this is the place to share news, strategies, and game analyses.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Melody Makers', 3, 'A haven for music lovers to discuss different genres, latest releases, and concerts.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Foodie Friends', 4, 'From recipes to restaurant reviews, connect with fellow foodies and share your culinary adventures.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Globe Trotters', 5, 'Join a community of travelers sharing experiences, tips, and photos from around the world.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Tech Innovators', 6, 'Discuss the latest in technology, from cutting-edge gadgets to software developments.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Artistic Minds', 1, 'Explore creativity and artistic expression in this community dedicated to the arts, from painting to sculpture.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Fitness Fanatics', 2, 'Join fellow fitness enthusiasts to share workout routines, diet tips, and motivation for a healthier lifestyle.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Soundtrack Junkies', 3, 'Love movie soundtracks? This community is for fans of film scores and soundtrack aficionados to discuss their favorite compositions.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Culinary Creators', 4, 'Share your passion for cooking and baking with a community of fellow culinary creators. Exchange recipes, cooking techniques, and culinary inspirations.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Book Worms', 7, 'A community for book lovers to discuss their favorite reads, authors, and literary genres.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Gaming Guild', 8, 'Join fellow gamers to discuss the latest games, strategies, and gaming news.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Photography Pros', 9, 'A community for photographers to share tips, techniques, and their best shots.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('DIY Enthusiasts', 10, 'Share your DIY projects, tips, and inspiration with a community of like-minded creators.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Pet Lovers', 11, 'Connect with fellow pet owners to share stories, tips, and advice on pet care.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Fashion Forward', 12, 'Discuss the latest trends, styles, and fashion news with a community of fashion enthusiasts.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Green Thumbs', 13, 'A community for gardeners to share tips, techniques, and their gardening successes.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('History Buffs', 14, 'Join a community of history enthusiasts to discuss historical events, figures, and eras.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Science Geeks', 15, 'Discuss the latest scientific discoveries, theories, and news with a community of science enthusiasts.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Language Learners', 16, 'Join a community of language learners to share tips, resources, and practice your language skills.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES ('Outdoor Adventurers', 17, 'Share your outdoor adventures, tips, and gear recommendations with a community of outdoor enthusiasts.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');


-- Request

INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'What a great movie!', 'Just watched the latest blockbuster at the Cinema Club. It was amazing!', 1, 1, 42, 18, 10, 22, '2024-04-22 05:23:36.747296', '2024-04-22 05:23:36.747314');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'Exciting game last night!', 'The All Sports Forum never disappoints. Let''s discuss last night''s game.', 2, 2, 34, 27, 15, 18, '2024-04-22 05:23:36.747296', '2024-04-22 05:23:36.747314');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'New favorite song!', 'Discovered a new track at Melody Makers. It''s been on repeat all day!', 3, 3, 57, 42, 20, 32, '2024-04-22 05:23:36.747296', '2024-04-22 05:23:36.747314');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'Amazing recipe find!', 'Found the most delicious recipe at Foodie Friends. Can''t wait to try it out!', 4, 4, 71, 58, 30, 42, '2024-04-22 05:23:36.747296', '2024-04-22 05:23:36.747314');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'Dream destination', 'Globe Trotters inspired me to plan my next adventure. Where should I go next?', 5, 5, 89, 75, 40, 52, '2024-04-22 05:23:36.747296', '2024-04-22 05:23:36.747314');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'Tech innovation discussion', 'Tech Innovators always has the latest tech news. Let''s dive into the newest innovations.', 6, 6, 103, 90, 55, 62, '2024-04-22 05:23:36.747296', '2024-04-22 05:23:36.747314');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'Artistic expressions', 'Artistic Minds is a place for creative minds to share ideas and inspiration. Let''s create together!', 7, 1, 46, 35, 18, 28, '2024-04-22 05:23:36.747296', '2024-04-22 05:23:36.747314');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'Workout motivation needed', 'Looking for some motivation at Fitness Fanatics. Share your favorite workout routines!', 8, 2, 52, 41, 23, 36, '2024-04-22 05:23:36.747296', '2024-04-22 05:23:36.747314');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'Epic soundtrack discovery', 'Soundtrack Junkies introduced me to a new soundtrack. Can''t stop listening!', 9, 3, 65, 53, 28, 44, '2024-04-22 05:23:36.747296', '2024-04-22 05:23:36.747314');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'Creative cooking ideas', 'Culinary Creators shared some unique recipes. Let''s get cooking!', 10, 4, 79, 65, 35, 52, '2024-04-22 05:23:36.747296', '2024-04-22 05:23:36.747314');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('b4ef71f8-409f-485f-b797-b44b5853a1f5', 'Thrilling book recommendation', 'Bookworms United just recommended a gripping new novel. Can''t wait to dive in!', 11, 5, 92, 78, 45, 55, '2024-05-02 12:15:00', '2024-05-02 12:15:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('b4ef71f8-409f-485f-b797-b44b5853a1f5', 'Mind-bending puzzle challenge', 'Puzzle Enthusiasts just shared a brain-teasing puzzle. Let''s crack it together!', 12, 6, 105, 92, 60, 68, '2024-05-02 12:17:00', '2024-05-02 12:17:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('b4ef71f8-409f-485f-b797-b44b5853a1f5', 'Movie marathon suggestions', 'Film Buffs Society is discussing must-watch movies for a weekend marathon. Join the conversation!', 13, 1, 49, 38, 25, 32, '2024-05-02 12:19:00', '2024-05-02 12:19:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('b4ef71f8-409f-485f-b797-b44b5853a1f5', 'Healthy lifestyle tips', 'Health & Wellness Hub shared some valuable tips for maintaining a healthy lifestyle. Let''s prioritize our health!', 14, 2, 55, 44, 28, 36, '2024-05-02 12:21:00', '2024-05-02 12:21:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('b4ef71f8-409f-485f-b797-b44b5853a1f5', 'Travel photography inspiration', 'Shutterbugs Union just shared breathtaking travel photos. Feeling inspired to capture new moments!', 15, 3, 69, 57, 32, 48, '2024-05-02 12:23:00', '2024-05-02 12:23:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('b4ef71f8-409f-485f-b797-b44b5853a1f5', 'Discussion on AI ethics', 'AI Enthusiasts Forum is debating the ethical implications of AI technology. Join the conversation!', 16, 4, 83, 69, 38, 56, '2024-05-02 12:25:00', '2024-05-02 12:25:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('b4ef71f8-409f-485f-b797-b44b5853a1f5', 'Artistic movie recommendations', 'Cinephile Circle just recommended some visually stunning films. Can''t wait to experience them!', 17, 5, 97, 84, 48, 62, '2024-05-02 12:27:00', '2024-05-02 12:27:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('b4ef71f8-409f-485f-b797-b44b5853a1f5', 'Gardening tips and tricks', 'Green Thumbs Society shared some expert gardening advice. Time to make our gardens flourish!', 18, 6, 111, 98, 65, 72, '2024-05-02 12:29:00', '2024-05-02 12:29:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('b4ef71f8-409f-485f-b797-b44b5853a1f5', 'Discussion on renewable energy', 'Renewable Energy Enthusiasts are discussing the latest advancements in renewable energy sources. Join the conversation!', 19, 1, 53, 42, 30, 40, '2024-05-02 12:31:00', '2024-05-02 12:31:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('b4ef71f8-409f-485f-b797-b44b5853a1f5', 'Virtual reality gaming experiences', 'VR Enthusiasts just shared their latest virtual reality gaming experiences. Let''s explore new worlds together!', 20, 2, 61, 49, 35, 44, '2024-05-02 12:33:00', '2024-05-02 12:33:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 'Exciting new hiking trail!', 'Just discovered a breathtaking new trail in the mountains. Who''s up for an adventure?', 1, 1, 20, 8, 5, 12, '2024-05-03 09:30:00', '2024-05-03 09:30:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 'New gaming console release!', 'Gamer''s Paradise just announced the release of the latest gaming console. Let''s discuss the features and games!', 2, 2, 15, 12, 8, 10, '2024-05-03 10:00:00', '2024-05-03 10:00:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 'New painting masterpiece', 'Art Enthusiasts just unveiled a stunning new painting. Let''s appreciate the art together!', 3, 3, 30, 20, 10, 18, '2024-05-03 11:30:00', '2024-05-03 11:30:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 'Fitness challenge!', 'Join the Fitness Challenge group and let''s motivate each other to achieve our fitness goals!', 4, 4, 25, 18, 12, 15, '2024-05-03 13:00:00', '2024-05-03 13:00:00');
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES ('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 'Exciting new music album!', 'Music Lovers just released a hot new album. Let''s share our favorite tracks!', 5, 5, 40, 32, 18, 25, '2024-05-03 14:30:00', '2024-05-03 14:30:00');


-- Reply

INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (1, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'I agree! The movie was fantastic.', 'HUMAN', 12, 8, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (1, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'I think the ending was a bit predictable, but overall it was enjoyable.', 'HUMAN', 6, 3, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (2, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'The game last night was intense! Did you see that winning goal?', 'HUMAN', 25, 15, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (2, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'I missed the game, but I heard about that goal! Sounds like it was amazing.', 'HUMAN', 8, 5, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (3, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'I love this song! It always puts me in a good mood.', 'HUMAN', 18, 10, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (3, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'The lyrics are so meaningful. It''s one of my favorites.', 'HUMAN', 14, 7, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (4, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'That recipe looks delicious! I''m definitely going to try making it this weekend.', 'HUMAN', 32, 20, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (4, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'I made this last week and it turned out great! Highly recommend it.', 'HUMAN', 28, 18, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (5, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'Traveling is such an amazing experience. I''ve been to some incredible places.', 'HUMAN', 45, 30, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (5, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'I agree! It''s always so exciting to explore new cultures and landscapes.', 'HUMAN', 38, 25, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (11, 'b4ef71f8-409f-485f-b797-b44b5853a1f5', 'I completely agree with your recommendation! That book had me hooked from the first page.', 'AI', 16, 12, '2024-05-02 12:40:00', '2024-05-02 12:40:00');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (11, 'b4ef71f8-409f-485f-b797-b44b5853a1f5', 'The plot twists kept me guessing until the very end. It was an exhilarating read!', 'HUMAN', 22, 18, '2024-05-02 12:42:00', '2024-05-02 12:42:00');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (12, 'b4ef71f8-409f-485f-b797-b44b5853a1f5', 'That puzzle was indeed challenging! It took me a while to figure it out, but it was so satisfying once I did.', 'HUMAN', 30, 22, '2024-05-02 12:44:00', '2024-05-02 12:44:00');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (12, 'b4ef71f8-409f-485f-b797-b44b5853a1f5', 'I love puzzles that really make you think. It''s a great way to exercise the brain!', 'AI', 18, 15, '2024-05-02 12:46:00', '2024-05-02 12:46:00');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (13, 'b4ef71f8-409f-485f-b797-b44b5853a1f5', 'I missed the game, but I heard it was a nail-biter! Looking forward to catching the highlights.', 'HUMAN', 28, 20, '2024-05-02 12:48:00', '2024-05-02 12:48:00');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (13, 'b4ef71f8-409f-485f-b797-b44b5853a1f5', 'The game definitely lived up to the hype! Can''t wait to see the replays.', 'AI', 24, 18, '2024-05-02 12:50:00', '2024-05-02 12:50:00');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (14, 'b4ef71f8-409f-485f-b797-b44b5853a1f5', 'Those tips are so helpful! Implementing them into my routine starting today.', 'HUMAN', 36, 28, '2024-05-02 12:52:00', '2024-05-02 12:52:00');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (14, 'b4ef71f8-409f-485f-b797-b44b5853a1f5', 'I''ve already noticed a positive difference in my energy levels since following those tips. Thanks for sharing!', 'AI', 42, 35, '2024-05-02 12:54:00', '2024-05-02 12:54:00');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (15, 'b4ef71f8-409f-485f-b797-b44b5853a1f5', 'Traveling opens up a world of possibilities! It''s such a fulfilling experience.', 'HUMAN', 48, 40, '2024-05-02 12:56:00', '2024-05-02 12:56:00');
INSERT INTO reply (request_id, replier_id, content, source, like_num, save_num, create_at, update_at) VALUES (15, 'b4ef71f8-409f-485f-b797-b44b5853a1f5', 'Absolutely! Each destination offers something unique and memorable.', 'AI', 52, 45, '2024-05-02 12:58:00', '2024-05-02 12:58:00');

-- Treading

INSERT INTO trending (request_id, author_id, reply_num, date, update_at) VALUES (1, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 65, '2024-04-22', '2024-04-22 05:36:18.811157');
INSERT INTO trending (request_id, author_id, reply_num, date, update_at) VALUES (2, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 50, '2024-04-22', '2024-04-22 05:36:18.811157');
INSERT INTO trending (request_id, author_id, reply_num, date, update_at) VALUES (3, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 24, '2024-04-22', '2024-04-22 05:36:18.811157');
INSERT INTO trending (request_id, author_id, reply_num, date, update_at) VALUES (4, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 45, '2024-04-22', '2024-04-22 05:36:18.811157');
INSERT INTO trending (request_id, author_id, reply_num, date, update_at) VALUES (5, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 84, '2024-04-22', '2024-04-22 05:36:18.811157');
INSERT INTO trending (request_id, author_id, reply_num, date, update_at) VALUES (6, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 5, '2024-04-22', '2024-04-22 05:36:18.811157');
INSERT INTO trending (request_id, author_id, reply_num, date, update_at) VALUES (7, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 26, '2024-04-22', '2024-04-22 05:36:18.811157');
INSERT INTO trending (request_id, author_id, reply_num, date, update_at) VALUES (8, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 18, '2024-04-22', '2024-04-22 05:36:18.811157');
INSERT INTO trending (request_id, author_id, reply_num, date, update_at) VALUES (9, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 68, '2024-04-22', '2024-04-22 05:36:18.811157');
INSERT INTO trending (request_id, author_id, reply_num, date, update_at) VALUES (10, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 43, '2024-04-22', '2024-04-22 05:36:18.811157');

-- Category

INSERT INTO category (name, create_at) VALUES ('movie', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('sports', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('music', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('food', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('travel', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('technology', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('education', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('health', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('fashion', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('art', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('science', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('business', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('history', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('nature', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('photography', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('cooking', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('gardening', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('culture', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('literature', '2024-04-22 05:36:18.786973');
INSERT INTO category (name, create_at) VALUES ('football', '2024-04-22 05:36:18.786973');

-- Tag

INSERT INTO tag (name, create_at) VALUES ('LossRecovery', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('QuestionCreation', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('QuizMaking', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('ProblemSolving', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('CreativeChallenges', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('AnalyticalThinking', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('KnowledgeSeeking', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('LearningJourney', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('TestPreparation', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('BrainTeasers', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('LogicalReasoning', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('DataAnalysis', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('CriticalThinking', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('MemoryEnhancement', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('DecisionMaking', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('ProblemIdentification', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('SkillDevelopment', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('CognitiveTraining', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('ResearchSkills', '2024-04-22 05:23:36.749344');
INSERT INTO tag (name, create_at) VALUES ('MindMapping', '2024-04-22 05:23:36.749344');
