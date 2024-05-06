-- 创建相册表
CREATE TABLE Albums (
    AlbumID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    AlbumName VARCHAR(100) NOT NULL,
    Description TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
-- 创建照片表
CREATE TABLE Photos (
    PhotoID INT PRIMARY KEY AUTO_INCREMENT,
    AlbumID INT,
    PhotoName VARCHAR(100) NOT NULL,
    Description TEXT,
    FilePath VARCHAR(255) NOT NULL,
    UploadedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID)
);
-- 创建权限表
CREATE TABLE Permissions (
    UserID INT,
    AlbumID INT,
    PermissionType ENUM('read', 'write'),
    PRIMARY KEY (UserID, AlbumID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID)
);

-- 创建活动日志表
CREATE TABLE ActivityLog (
    LogID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    ActivityDescription TEXT NOT NULL,
    ActivityDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
