USE cemetery;

CREATE TABLE `PaymentDetails` (
    `PaymentDetailsID` INT AUTO_INCREMENT NOT NULL,
    `PlotDetailsID` INT NOT NULL,
    `DeceasedDetailsID` INT NOT NULL,
    `ContactDetailsID` INT NOT NULL,
    `PaymentStatusID` INT NOT NULL,
    `BalancePaid` DECIMAL(10,2) NOT NULL,
    `BalanceDue` DECIMAL(10,2) NOT NULL,
    `DatePaid` DATETIME NOT NULL,
    `NoteID` INT NULL,
    `CreatedDate` DATETIME NOT NULL,
    `CreatedBy` INT NOT NULL,
    `ModifiedDate` DATETIME NULL,
    `ModifiedBy` INT NULL,
    PRIMARY KEY (`PaymentDetailsID`)
) ENGINE=InnoDB;

-- Indexes
CREATE INDEX `ix_PlotPaymentStatus` ON `PaymentDetails` (`PlotID`, `PaymentStatusID`);
CREATE INDEX `ix_DeceasedDetails` ON `PaymentDetails` (`DeceasedDetailsID`);
CREATE INDEX `ix_ContactPaymentDetails` ON `PaymentDetails` (`ContactDetailsID`);
CREATE INDEX `ix_DatePaid` ON `PaymentDetails` (`DatePaid`);

-- Foreign Keys
ALTER TABLE `PaymentDetails`
ADD CONSTRAINT `FK_PaymentDetails_PlotDetails` FOREIGN KEY (`PlotDetailsID`) REFERENCES `PlotDetails`(`PlotID`),
ADD CONSTRAINT `FK_PaymentDetails_DeceasedDetails` FOREIGN KEY (`DeceasedDetailsID`) REFERENCES `DeceasedDetails`(`DeceasedDetailsID`),
ADD CONSTRAINT `FK_PaymentDetails_PaymentStatus` FOREIGN KEY (`PaymentStatusID`) REFERENCES `PaymentStatus`(`PaymentStatusID`),
ADD CONSTRAINT `FK_PaymentDetails_ContactDetails` FOREIGN KEY (`ContactDetailsID`) REFERENCES `ContactDetails`(`ContactDetailsID`),
ADD CONSTRAINT `FK_PaymentDetails_Notes` FOREIGN KEY (`NoteID`) REFERENCES `Notes`(`NoteID`),
ADD CONSTRAINT `FK_PaymentDetails_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users`(`UserID`),
ADD CONSTRAINT `FK_PaymentDetails_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users`(`UserID`);
