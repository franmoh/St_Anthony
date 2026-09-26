USE cemetery;

CREATE TABLE `DeceasedStatus` (
    `DeceasedStatusID` INT AUTO_INCREMENT NOT NULL,
    `DeceasedStatusConstant` VARCHAR(100) NOT NULL,
    `CreatedDate` DATETIME NOT NULL,
    `CreatedBy` INT NOT NULL,
    `ModifiedDate` DATETIME NULL,
    `ModifiedBy` INT NULL,
    PRIMARY KEY (`DeceasedStatusID`)
) ENGINE=InnoDB;

-- Indexes
CREATE UNIQUE INDEX `ixDeceasedStatusConstant`
ON `DeceasedStatus` (`DeceasedStatusConstant`);

-- Foreign keys
ALTER TABLE `DeceasedStatus`
ADD CONSTRAINT `FK_DeceasedStatus_CreatedBy`
FOREIGN KEY (`CreatedBy`) REFERENCES `Users`(`UserID`),
ADD CONSTRAINT `FK_DeceasedStatus_ModifiedBy`
FOREIGN KEY (`ModifiedBy`) REFERENCES `Users`(`UserID`);
