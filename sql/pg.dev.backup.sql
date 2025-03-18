-- Create UUID extension if not exists
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User
CREATE TABLE IF NOT EXISTS "user" (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120),
    password_hash VARCHAR(300),
    avatar_url VARCHAR(300),
    use_google BOOLEAN DEFAULT FALSE,
    use_github BOOLEAN DEFAULT FALSE,
    security_question VARCHAR(100),
    security_answer VARCHAR(100),
    status VARCHAR(20) DEFAULT 'ACTIVE',
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Preference
CREATE TABLE IF NOT EXISTS user_preference (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL UNIQUE REFERENCES "user"(id),
    communities VARCHAR(200),
    interests VARCHAR(200),
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Record
CREATE TABLE IF NOT EXISTS user_record (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES "user"(id),
    request_id INTEGER NOT NULL,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Like
CREATE TABLE IF NOT EXISTS user_like (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES "user"(id),
    request_id INTEGER NOT NULL,
    reply_id INTEGER,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Save
CREATE TABLE IF NOT EXISTS user_save (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES "user"(id),
    request_id INTEGER NOT NULL,
    reply_id INTEGER,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Notice
CREATE TABLE IF NOT EXISTS user_notice (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES "user"(id),
    subject VARCHAR(100) NOT NULL,
    content VARCHAR(1000) DEFAULT '',
    module VARCHAR(50) DEFAULT 'SYSTEM',
    status BOOLEAN DEFAULT FALSE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Community
CREATE TABLE IF NOT EXISTS community (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    category_id INTEGER,
    description VARCHAR(500),
    avatar_url VARCHAR(300),
    creator_id VARCHAR(36) REFERENCES "user"(id),
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Request
CREATE TABLE IF NOT EXISTS request (
    id SERIAL PRIMARY KEY,
    author_id VARCHAR(36) NOT NULL REFERENCES "user"(id),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    community_id INTEGER REFERENCES community(id),
    tag_id INTEGER,
    view_num INTEGER DEFAULT 0,
    like_num INTEGER DEFAULT 0,
    reply_num INTEGER DEFAULT 0,
    save_num INTEGER DEFAULT 0,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reply
CREATE TABLE IF NOT EXISTS reply (
    id SERIAL PRIMARY KEY,
    request_id INTEGER NOT NULL REFERENCES request(id),
    replier_id VARCHAR(36) NOT NULL REFERENCES "user"(id),
    reply_id INTEGER REFERENCES reply(id),
    content VARCHAR(1000),
    source VARCHAR(50) DEFAULT 'HUMAN',
    like_num INTEGER DEFAULT 0,
    save_num INTEGER DEFAULT 0,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trending
CREATE TABLE IF NOT EXISTS trending (
    id SERIAL PRIMARY KEY,
    request_id INTEGER NOT NULL UNIQUE REFERENCES request(id),
    author_id VARCHAR(36) NOT NULL REFERENCES "user"(id),
    view_num INTEGER DEFAULT 0,
    reply_num INTEGER DEFAULT 0,
    date VARCHAR(10) DEFAULT CURRENT_DATE,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Category
CREATE TABLE IF NOT EXISTS category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tag
CREATE TABLE IF NOT EXISTS tag (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
-- User data
INSERT INTO "user" (id, username, email, password_hash, avatar_url, use_google, use_github, security_question, security_answer, status, create_at, update_at) VALUES 
('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'tonglam', 'bluedragon00000@gmail.com', '$2b$12$R49DZkkWelMYoCv2.mCQeemIVKkCNrzuA3Vekq6PxMpIk4jqjJbmW', 'https://avatars.githubusercontent.com/u/19681829?v=4', true, true, 'What is your favorite color?', 'blue', 'ACTIVE', '2024-04-21 14:36:18.896100', '2024-04-21 15:31:20.425434'),
('b4ef71f8-409f-485f-b797-b44b5853a1f5', 'tonglan', 'qitonglan@gmail.com', '$2b$12$D7uO.K4xHTA62nmLd/WM4ODTeAU2tP/aGVFQf9o7HpdfKNdryF2Oi', 'https://www.gravatar.com/avatar/4ad8c50f623b6eccf0299d12005d39e7b670ac7e49654ee662016ba1c1915b54', false, false, 'Which color?', 'blue', 'ACTIVE', '2024-05-02 11:50:58.257018', '2024-05-02 11:50:58.257040'),
('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 'Hayeensss', null, null, 'https://avatars.githubusercontent.com/u/145556077?v=4', false, true, '', '', 'ACTIVE', '2024-05-07 11:35:01.583653', '2024-05-07 11:35:01.583673');

-- User Preference data
INSERT INTO user_preference (user_id, communities, interests, update_at) VALUES 
('ab9ef73b-14bf-4031-a199-2ae67ce7f341', '1,3,5,7,9', '1,3,5,7', '2024-04-22 05:36:18.811157');

-- Category data
INSERT INTO category (name, create_at) VALUES 
('movie', '2024-04-22 05:36:18.786973'),
('sports', '2024-04-22 05:36:18.786973'),
('music', '2024-04-22 05:36:18.786973'),
('food', '2024-04-22 05:36:18.786973'),
('travel', '2024-04-22 05:36:18.786973'),
('technology', '2024-04-22 05:36:18.786973'),
('education', '2024-04-22 05:36:18.786973'),
('health', '2024-04-22 05:36:18.786973'),
('fashion', '2024-04-22 05:36:18.786973'),
('art', '2024-04-22 05:36:18.786973');

-- Tag data
INSERT INTO tag (name, create_at) VALUES 
('LossRecovery', '2024-04-22 05:23:36.749344'),
('QuestionCreation', '2024-04-22 05:23:36.749344'),
('QuizMaking', '2024-04-22 05:23:36.749344'),
('ProblemSolving', '2024-04-22 05:23:36.749344'),
('CreativeChallenges', '2024-04-22 05:23:36.749344'),
('AnalyticalThinking', '2024-04-22 05:23:36.749344'),
('KnowledgeSeeking', '2024-04-22 05:23:36.749344'),
('LearningJourney', '2024-04-22 05:23:36.749344'),
('TestPreparation', '2024-04-22 05:23:36.749344'),
('BrainTeasers', '2024-04-22 05:23:36.749344');

-- Community data
INSERT INTO community (name, category_id, description, avatar_url, creator_id, create_at, update_at) VALUES 
('Cinema Club', 1, 'A community for movie enthusiasts to discuss the latest films, classic cinema, and film industry trends.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436'),
('All Sports Forum', 2, 'Whether you''re into football, basketball, or swimming, this is the place to share news, strategies, and game analyses.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'b4ef71f8-409f-485f-b797-b44b5853a1f5', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436'),
('Melody Makers', 3, 'A haven for music lovers to discuss different genres, latest releases, and concerts.', 'https://i.ibb.co/h7rq9BF/profile-picture.jpg', 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');

-- Request data
INSERT INTO request (author_id, title, content, community_id, tag_id, view_num, like_num, reply_num, save_num, create_at, update_at) VALUES 
('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'What a great movie!', 'Just watched the latest blockbuster at the Cinema Club. It was amazing!', 1, 1, 42, 18, 10, 22, '2024-04-22 05:23:36.747296', '2024-04-22 05:23:36.747314'),
('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'Exciting game last night!', 'The All Sports Forum never disappoints. Let''s discuss last night''s game.', 2, 2, 34, 27, 15, 18, '2024-04-22 05:23:36.747296', '2024-04-22 05:23:36.747314'),
('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'New favorite song!', 'Discovered a new track at Melody Makers. It''s been on repeat all day!', 3, 3, 57, 42, 20, 32, '2024-04-22 05:23:36.747296', '2024-04-22 05:23:36.747314');

-- Reply data
INSERT INTO reply (request_id, replier_id, reply_id, content, source, like_num, save_num, create_at, update_at) VALUES 
(1, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', NULL, 'I agree! The movie was fantastic.', 'HUMAN', 12, 8, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436'),
(1, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', NULL, 'I think the ending was a bit predictable, but overall it was enjoyable.', 'HUMAN', 6, 3, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436'),
(2, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', NULL, 'The game last night was intense! Did you see that winning goal?', 'HUMAN', 25, 15, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');

-- Then insert child replies referencing the parent replies
INSERT INTO reply (request_id, replier_id, reply_id, content, source, like_num, save_num, create_at, update_at) VALUES 
(1, 'b4ef71f8-409f-485f-b797-b44b5853a1f5', 1, 'Yes, especially the special effects!', 'HUMAN', 5, 2, '2024-04-22 05:24:36.740414', '2024-04-22 05:24:36.740436'),
(1, 'ffe8b047-84a8-45a5-9f15-e573b1e1041a', 2, 'I had the same feeling about the ending.', 'HUMAN', 4, 1, '2024-04-22 05:25:36.740414', '2024-04-22 05:25:36.740436'),
(2, 'b4ef71f8-409f-485f-b797-b44b5853a1f5', 3, 'That last-minute goal was incredible!', 'HUMAN', 8, 3, '2024-04-22 05:26:36.740414', '2024-04-22 05:26:36.740436');

-- User Record data
INSERT INTO user_record (user_id, request_id, create_at) VALUES 
('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 1, '2024-04-22 05:23:36.740414'),
('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 2, '2024-04-22 05:23:36.740414'),
('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 3, '2024-04-22 05:23:36.740414');

-- User Like data
INSERT INTO user_like (user_id, request_id, reply_id, create_at) VALUES 
('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 1, 2, '2024-05-03 09:30:00'),
('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 2, 1, '2024-05-03 10:00:00'),
('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 3, 4, '2024-05-03 11:30:00');

-- User Save data
INSERT INTO user_save (user_id, request_id, reply_id, create_at) VALUES 
('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 1, 1, '2024-04-22 05:23:36.740414'),
('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 2, 4, '2024-04-22 05:23:36.740414'),
('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 3, 4, '2024-04-22 05:23:36.740414');

-- User Notice data
INSERT INTO user_notice (user_id, subject, content, module, status, create_at, update_at) VALUES
('ab9ef73b-14bf-4031-a199-2ae67ce7f341', 'Welcome!', 'Welcome to ASKIFY!', 'SYSTEM', false, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436'),
('b4ef71f8-409f-485f-b797-b44b5853a1f5', 'New Reply', 'Someone replied to your post', 'POST', false, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436'),
('ffe8b047-84a8-45a5-9f15-e573b1e1041a', 'Profile Update', 'Your profile was updated successfully', 'USER', true, '2024-04-22 05:23:36.740414', '2024-04-22 05:23:36.740436');

-- Trending data
INSERT INTO trending (request_id, author_id, view_num, reply_num, date, update_at) VALUES 
(1, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 65, 42, '2024-04-22', '2024-04-22 05:36:18.811157'),
(2, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 50, 35, '2024-04-22', '2024-04-22 05:36:18.811157'),
(3, 'ab9ef73b-14bf-4031-a199-2ae67ce7f341', 24, 18, '2024-04-22', '2024-04-22 05:36:18.811157'); 