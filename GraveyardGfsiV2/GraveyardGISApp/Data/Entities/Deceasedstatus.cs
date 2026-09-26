using System;
using System.Collections.Generic;

namespace GraveyardGISApp.Data.Entities;

public partial class Deceasedstatus
{
    public int DeceasedStatusId { get; set; }

    public string DeceasedStatusConstant { get; set; } = null!;

    public DateTime CreatedDate { get; set; }

    public int CreatedBy { get; set; }

    public DateTime ModifiedDate { get; set; }

    public int ModifiedBy { get; set; }
}
