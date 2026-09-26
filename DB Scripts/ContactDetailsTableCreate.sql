USE cemetery;

CREATE TABLE `ContactDetails` (
    `ContactDetailsID` INT AUTO_INCREMENT NOT NULL,
    `PlotDetailsID` INT NOT NULL,
    `DeceasedDetailsID` INT NOT NULL,
    `FirstName` VARCHAR(100) NOT NULL,
    `LastName` VARCHAR(100) NOT NULL,
    `PhoneNumber` VARCHAR(100) NULL,
    `Address` VARCHAR(100) NULL,
    `Email` VARCHAR(100) NULL,
    `NoteID` INT NULL,
    `CreatedDate` DATETIME NOT NULL,
    `CreatedBy` INT NOT NULL,
    `ModifiedDate` DATETIME NULL,
    `ModifiedBy` INT NULL,
    PRIMARY KEY (`ContactDetailsID`)
) ENGINE=InnoDB;

-- Indexes
CREATE INDEX `ix_PlotMaintenanceDetails` 
ON `ContactDetails` (`PlotID`, `DeceasedDetailsID`);

-- Foreign keys
ALTER TABLE `ContactDetails`
ADD CONSTRAINT `FK_ContactDetails_Plot`
FOREIGN KEY (`PlotID`) REFERENCES `PlotDetails`(`PlotDetailsID`),
ADD CONSTRAINT `FK_ContactDetails_Status`
FOREIGN KEY (`DeceasedDetailsID`) REFERENCES `DeceasedDetails`(`DeceasedDetailsID`),
ADD CONSTRAINT `FK_ContactDetails_Notes`
FOREIGN KEY (`NoteID`) REFERENCES `Notes`(`NoteID`),
ADD CONSTRAINT `FK_ContactDetails_CreatedBy`
FOREIGN KEY (`CreatedBy`) REFERENCES `Users`(`UserID`),
ADD CONSTRAINT `FK_ContactDetails_ModifiedBy`
FOREIGN KEY (`ModifiedBy`) REFERENCES `Users`(`UserID`);
