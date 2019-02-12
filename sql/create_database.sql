CREATE DATABASE IF NOT EXISTS flaskd3;
USE flaskd3;
GRANT ALL ON flaskd3.* TO flaskd3@"%" IDENTIFIED BY "flaskd3";
GRANT SELECT ON flaskd3.* TO read_only@"%" IDENTIFIED BY "read_only";