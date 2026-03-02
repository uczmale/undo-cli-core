CREATE DATABASE IF NOT EXISTS undo_<ENV>;

CREATE USER IF NOT EXISTS undo_admin_<ENV> IDENTIFIED BY '<ADMIN_PASSWORD>';
GRANT ALL PRIVILEGES ON undo_<ENV>.* TO undo_admin_<ENV>;

ALTER USER undo_admin_<ENV> IDENTIFIED WITH mysql_native_password
BY '<ADMIN_PASSWORD>';

CREATE USER IF NOT EXISTS undo_user_<ENV> IDENTIFIED BY '<USER_PASSWORD>';
ALTER USER undo_user_<ENV> IDENTIFIED WITH mysql_native_password
BY '<USER_PASSWORD>';

FLUSH PRIVILEGES;

-- DROP TABLE undo_<ENV>.undo_t_shoutout;
CREATE TABLE IF NOT EXISTS undo_<ENV>.undo_t_command (
    identifier              INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    contributor_identifier  VARCHAR(10) NOT NULL,
    content                 TEXT NOT NULL,
    type_identifier         INT,
    created_timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

