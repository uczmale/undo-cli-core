CREATE DATABASE IF NOT EXISTS spotlight_<ENV>;

CREATE USER IF NOT EXISTS spotlight_admin_<ENV> IDENTIFIED BY '<ADMIN_PASSWORD>';
GRANT ALL PRIVILEGES ON spotlight_<ENV>.* TO spotlight_admin_<ENV>;

ALTER USER spotlight_admin_<ENV> IDENTIFIED WITH mysql_native_password
BY '<ADMIN_PASSWORD>';

CREATE USER IF NOT EXISTS spotlight_user_<ENV> IDENTIFIED BY '<USER_PASSWORD>';
ALTER USER spotlight_user_<ENV> IDENTIFIED WITH mysql_native_password
BY '<USER_PASSWORD>';

FLUSH PRIVILEGES;

-- DROP TABLE spotlight_<ENV>.spotlight_t_shoutout;
CREATE TABLE IF NOT EXISTS spotlight_<ENV>.spotlight_t_shoutout (
    identifier              INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    contributor_identifier  VARCHAR(10) NOT NULL,
    content                 TEXT NOT NULL,
    type_identifier         INT,
    created_timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

