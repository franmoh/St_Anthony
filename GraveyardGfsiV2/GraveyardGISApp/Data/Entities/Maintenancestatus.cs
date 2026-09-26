using System;
using System.Collections.Generic;

namespace GraveyardGISApp.Data.Entities;

public partial class Maintenancestatus
{
    public int MaintenanceStatusId { get; set; }

    public string MaintenanceStatusConstant { get; set; } = null!;

    public DateTime CreatedDate { get; set; }

    public int CreatedBy { get; set; }

    public DateTime ModifiedDate { get; set; }

    public int ModifiedBy { get; set; }

    public virtual ICollection<Maintenancedetail> Maintenancedetails { get; set; } = new List<Maintenancedetail>();

    public virtual ICollection<Plotdetail> Plotdetails { get; set; } = new List<Plotdetail>();
}
