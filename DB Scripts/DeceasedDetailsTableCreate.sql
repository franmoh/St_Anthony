USE cemetery;

CREATE TABLE `DeceasedDetails` (
    `DeceasedDetailsID` INT AUTO_INCREMENT NOT NULL,
    `PlotDetailsID` INT NOT NULL,
    `DeceasedStatusID` INT NOT NULL,
    `FirstName` VARCHAR(100) NOT NULL,
    `LastName` VARCHAR(100) NOT NULL,
    `Initial` VARCHAR(100) NOT NULL,
    `DateBuried` DATE NULL,
    `DOB` DATE NOT NULL,
    `DOD` DATE NULL,
    `ContactDetailsID` INT NOT NULL,
    `NoteID` INT NULL,
    `CreatedDate` DATETIME NOT NULL,
    `CreatedBy` INT NOT NULL,
    `ModifiedDate` DATETIME NULL,
    `ModifiedBy` INT NULL,
    PRIMARY KEY (`DeceasedDetailsID`)
) ENGINE=InnoDB;

-- Indexes
CREATE INDEX `ix_DeceasedPlotStatus` ON `DeceasedDetails` (`PlotID`, `DeceasedStatusID`);
CREATE INDEX `ix_DeceasedContactDetails` ON `DeceasedDetails` (`ContactDetailsID`);
CREATE INDEX `ix_DateBuried` ON `DeceasedDetails` (`DateBuried`);
CREATE INDEX `ix_DOB` ON `DeceasedDetails` (`DOB`);

-- Foreign Keys
ALTER TABLE `DeceasedDetails`
ADD CONSTRAINT `FK_DeceasedDetails_PlotDetails`
FOREIGN KEY (`PlotID`) REFERENCES `PlotDetails`(`PlotDetailsID`),
ADD CONSTRAINT `FK_DeceasedDetails_DeceasedStatus`
FOREIGN KEY (`DeceasedStatusID`) REFERENCES `DeceasedStatus`(`DeceasedStatusID`),
ADD CONSTRAINT `FK_DeceasedDetails_ContactDetails`
FOREIGN KEY (`ContactDetailsID`) REFERENCES `ContactDetails`(`ContactDetailsID`),
ADD CONSTRAINT `FK_DeceasedDetails_Notes`
FOREIGN KEY (`NoteID`) REFERENCES `Notes`(`NoteID`),
ADD CONSTRAINT `FK_DeceasedDetails_CreatedBy`
FOREIGN KEY (`CreatedBy`) REFERENCES `Users`(`UserID`),
ADD CONSTRAINT `FK_DeceasedDetails_ModifiedBy`
FOREIGN KEY (`ModifiedBy`) REFERENCES `Users`(`UserID`);
