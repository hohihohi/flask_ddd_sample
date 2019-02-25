CREATE TABLE data_types (
    name VARCHAR(16) PRIMARY KEY
) Engine=InnoDB CHARSET=utf8mb4;

INSERT INTO data_types(name) VALUES ('raw');
INSERT INTO data_types(name) VALUES ('preprocessed');
INSERT INTO data_types(name) VALUES ('predicted');

CREATE TABLE regions (
    name VARCHAR(16) PRIMARY KEY
) Engine=InnoDB CHARSET=utf8mb4;

INSERT INTO regions (name) VALUES ('jp-east-1');

CREATE TABLE buckets(
    id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id    VARCHAR(16) NOT NULL,
    name       VARCHAR(32) NOT NULL,
    region     VARCHAR(16) NOT NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted_at DATETIME(6) NOT NULL DEFAULT '9999-12-31 23:59:59',
    UNIQUE unq_bucket_user_id_name_region (user_id, name, region, deleted_at),
    CONSTRAINT bucket_region_fk FOREIGN KEY (region) REFERENCES regions (name) ON UPDATE CASCADE
) Engine=InnoDB CHARSET=utf8mb4;

CREATE TABLE objects (
    id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id    VARCHAR(16) NOT NULL,
    name       VARCHAR(32) NOT NULL,
    region     VARCHAR(16) NOT NULL,
    version    VARCHAR(32) NOT NULL,
    bucket_id  INT UNSIGNED NOT NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted_at DATETIME(6) NOT NULL DEFAULT '9999-12-31 23:59:59',
    UNIQUE unq_name_version (name, version, deleted_at),
    CONSTRAINT object_region_fk FOREIGN KEY (region) REFERENCES regions (name) ON UPDATE CASCADE,
    CONSTRAINT object_bucket_id_fk FOREIGN KEY (bucket_id) REFERENCES buckets (id) ON UPDATE CASCADE
) Engine=InnoDB CHARSET=utf8mb4;

CREATE TABLE data (
    id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id    VARCHAR(16) NOT NULL,
    name       VARCHAR(32) NOT NULL,
    data_type  VARCHAR(16) NOT NULL,
    object_id  INT UNSIGNED NOT NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted_at DATETIME(6) NOT NULL DEFAULT '9999-12-31 23:59:59',
    UNIQUE unq_user_id_name (user_id, name, deleted_at),
    CONSTRAINT data_type_fk FOREIGN KEY (data_type) REFERENCES data_types (name) ON UPDATE CASCADE,
    CONSTRAINT data_object_id_fk FOREIGN KEY (object_id) REFERENCES objects (id) ON UPDATE CASCADE
) Engine=InnoDB CHARSET=utf8mb4;