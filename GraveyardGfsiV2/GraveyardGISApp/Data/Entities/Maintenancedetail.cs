using System;
using System.Collections.Generic;

namespace GraveyardGISApp.Data.Entities;

public partial class Maintenancedetail
{
    public int MaintId { get; set; }

    public string Description { get; set; } = null!;

    public int PlotDetailsId { get; set; }

    public int MaintenanceStatusId { get; set; }

    public DateTime CreatedDate { get; set; }

    public int CreatedBy { get; set; }

    public DateTime ModifiedDate { get; set; }

    public int ModifiedBy { get; set; }

    public virtual Maintenancestatus MaintenanceStatus { get; set; } = null!;

    public virtual ICollection<Note> Notes { get; set; } = new List<Note>();

    public virtual Plotdetail PlotDetails { get; set; } = null!;
}
