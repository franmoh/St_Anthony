USE cemetery

CREATE TABLE `MaintenanceStatus` (
    `MaintenanceStatusID` INT AUTO_INCREMENT NOT NULL,
    `MaintenanceStatusConstant` VARCHAR(100) NOT NULL,
    `CreatedDate` DATETIME NOT NULL,
    `CreatedBy` INT NOT NULL,
    `ModifiedDate` DATETIME NULL,
    `ModifiedBy` INT NULL,
    PRIMARY KEY (`MaintenanceStatusID`)
) ENGINE=InnoDB;

-- Indexes
CREATE UNIQUE INDEX `ixMaintenanceStatusConstant` 
ON `MaintenanceStatus` (`MaintenanceStatusConstant`);

-- Foreign keys
ALTER TABLE `MaintenanceStatus`
ADD CONSTRAINT `FK_MaintenanceStatus_CreatedBy`
FOREIGN KEY (`CreatedBy`) REFERENCES `Users`(`UserID`),
ADD CONSTRAINT `FK_MaintenanceStatus_ModifiedBy`
FOREIGN KEY (`ModifiedBy`) REFERENCES `Users`(`UserID`);