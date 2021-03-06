DROP TABLE files;
DROP TABLE directories;
DROP TABLE ignored_objects;
DROP TABLE deleted_objects;
CREATE TABLE files (
    "path" TEXT PRIMARY KEY NOT NULL UNIQUE,
    "lastModified" DATETIME NOT NULL,
    "deleted" BOOLEAN NOT NULL,
    "toEncrypt" BOOLEAN NOT NULL,
    "lastSync" DATETIME,
    "encryptedPath" TEXT,
    "parent" TEXT NOT NULL
);
CREATE TABLE directories (
    "path" TEXT PRIMARY KEY NOT NULL UNIQUE,
    "lastModified" DATETIME NOT NULL,
    "deleted" BOOLEAN NOT NULL,
    "toEncrypt" BOOLEAN NOT NULL,
    "lastSync" DATETIME,
    "parent" TEXT
);
CREATE TABLE ignored_objects (
    "ignoredObjPath" TEXT PRIMARY KEY NOT NULL UNIQUE
);
CREATE TABLE deleted_objects (
    "deletedObjPath" TEXT PRIMARY KEY NOT NULL UNIQUE
);
--insert into directories values ('', '2016-01-01 1:00:00', 0, 0, null, null);
.exit