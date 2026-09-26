using System;
using System.Collections.Generic;

namespace GraveyardGISApp.Data.Entities;

public partial class Plotdetail
{
    public int PlotDetailsId { get; set; }

    public int? PlotId { get; set; }

    public int? SectionId { get; set; }

    public int? MaintenanceStatusId { get; set; }

    public int? NoteId { get; set; }

    public string? PlotStatus { get; set; }

    public bool IsAvailable { get; set; }

    public string? Row { get; set; }

    public string? Unit { get; set; }

    public string? Side { get; set; }

    public string? Niche { get; set; }

    public DateTime CreatedDate { get; set; }

    public int CreatedBy { get; set; }

    public DateTime ModifiedDate { get; set; }

    public int ModifiedBy { get; set; }

    public virtual ICollection<Plotdetail> InversePlot { get; set; } = new List<Plotdetail>();

    public virtual Maintenancestatus? MaintenanceStatus { get; set; }

    public virtual ICollection<Maintenancedetail> Maintenancedetails { get; set; } = new List<Maintenancedetail>();

    public virtual ICollection<Note> Notes { get; set; } = new List<Note>();

    public virtual ICollection<Paymentdetail> Paymentdetails { get; set; } = new List<Paymentdetail>();

    public virtual Plotdetail? Plot { get; set; }

    public virtual Section? Section { get; set; }
}
