-- Insert Script for the Section Table. UserID 1 is the admin.
/*
Descriptions:
C (Columnbarium)
G (Garden of Angels)
L (Lower)
M (Middle)
P (Paul Family Plots)
U (Upper)
W (Western)
*/
INSERT INTO `Section` (`SectionConstant`, `CreatedDate`, `CreatedBy`)
VALUES
     ('C', NOW(), 1)
    ,('G', NOW(), 1)
    ,('L', NOW(), 1)
    ,('M', NOW(), 1)
    ,('P', NOW(), 1)
    ,('U', NOW(), 1)
    ,('W', NOW(), 1);
