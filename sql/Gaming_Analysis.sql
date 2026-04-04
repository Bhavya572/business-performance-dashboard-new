
CREATE DATABASE gaming_analysis;

USE gaming_analysis;

CREATE TABLE gaming_data (
    record_id VARCHAR(20),
    age INT,
    gender VARCHAR(10),
    daily_gaming_hours FLOAT,
    game_genre VARCHAR(50),
    primary_game VARCHAR(100),
    gaming_platform VARCHAR(50),

    sleep_hours FLOAT,
    sleep_quality VARCHAR(20),
    sleep_disruption_frequency VARCHAR(20),

    academic_work_performance VARCHAR(20),
    grades_gpa FLOAT,
    work_productivity_score FLOAT,

    mood_state VARCHAR(30),
    mood_swing_frequency VARCHAR(20),

    withdrawal_symptoms VARCHAR(10),
    loss_of_other_interests VARCHAR(10),
    continued_despite_problems VARCHAR(10),

    eye_strain VARCHAR(10),
    back_neck_pain VARCHAR(10),

    weight_change_kg FLOAT,
    exercise_hours_weekly FLOAT,

    social_isolation_score INT,
    face_to_face_social_hours_weekly FLOAT,

    monthly_game_spending_usd FLOAT,
    years_gaming INT,

    gaming_addiction_risk_level VARCHAR(20)
);

#1.What is the distribution of users across addiction risk levels?
SELECT 
    gaming_addiction_risk_level,
    COUNT(*) AS user_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage_share
FROM gaming_data
GROUP BY gaming_addiction_risk_level
ORDER BY user_count DESC;


#2.How do average gaming hours differ by addiction risk level?
SELECT 
    gaming_addiction_risk_level,
    ROUND(AVG(daily_gaming_hours), 2) AS avg_daily_gaming_hours,
    MIN(daily_gaming_hours) AS min_hours,
    MAX(daily_gaming_hours) AS max_hours
FROM gaming_data
GROUP BY gaming_addiction_risk_level
ORDER BY avg_daily_gaming_hours DESC;

#3.How does monthly spending vary across risk levels?
SELECT 
    gaming_addiction_risk_level,
    ROUND(AVG(monthly_game_spending_usd), 2) AS avg_monthly_spending,
    ROUND(SUM(monthly_game_spending_usd), 2) AS total_spending
FROM gaming_data
GROUP BY gaming_addiction_risk_level
ORDER BY avg_monthly_spending DESC;

#4.Which game genres have the highest average addiction risk indicators?
SELECT 
    game_genre,
    ROUND(AVG(daily_gaming_hours), 2) AS avg_gaming_hours,
    ROUND(AVG(monthly_game_spending_usd), 2) AS avg_spending,
    ROUND(AVG(social_isolation_score), 2) AS avg_isolation_score,
    COUNT(*) AS total_users
FROM gaming_data
GROUP BY game_genre
ORDER BY avg_gaming_hours DESC, avg_spending DESC;

#5.What is the gender-wise distribution of addiction risk levels?
SELECT 
    gender,
    gaming_addiction_risk_level,
    COUNT(*) AS user_count
FROM gaming_data
GROUP BY gender, gaming_addiction_risk_level
ORDER BY gender, user_count DESC;

#6.Which users show the highest potential risk based on gaming hours, spending, and isolation?
SELECT 
    record_id,
    age,
    gender,
    game_genre,
    daily_gaming_hours,
    monthly_game_spending_usd,
    social_isolation_score,
    gaming_addiction_risk_level
FROM gaming_data
WHERE daily_gaming_hours >= 8
  AND monthly_game_spending_usd >= 150
  AND social_isolation_score >= 6
ORDER BY daily_gaming_hours DESC, monthly_game_spending_usd DESC;

#7.Which users spend more than the average spending of their own risk group?
SELECT 
    record_id,
    gaming_addiction_risk_level,
    monthly_game_spending_usd
FROM gaming_data g
WHERE monthly_game_spending_usd > (
    SELECT AVG(monthly_game_spending_usd)
    FROM gaming_data
    WHERE gaming_addiction_risk_level = g.gaming_addiction_risk_level
)
ORDER BY gaming_addiction_risk_level, monthly_game_spending_usd DESC;

#8.Rank users by spending within each addiction risk level
SELECT 
    record_id,
    gaming_addiction_risk_level,
    monthly_game_spending_usd,
    RANK() OVER (
        PARTITION BY gaming_addiction_risk_level
        ORDER BY monthly_game_spending_usd DESC
    ) AS spending_rank_within_risk
FROM gaming_data
ORDER BY gaming_addiction_risk_level, spending_rank_within_risk;


#9.What are the top 3 genres with the highest average daily gaming hours?
SELECT *
FROM (
    SELECT 
        game_genre,
        ROUND(AVG(daily_gaming_hours), 2) AS avg_gaming_hours,
        DENSE_RANK() OVER (ORDER BY AVG(daily_gaming_hours) DESC) AS genre_rank
    FROM gaming_data
    GROUP BY game_genre
) ranked_genres
WHERE genre_rank <= 3
ORDER BY genre_rank;


