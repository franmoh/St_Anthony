using System;
using System.Collections.Generic;

namespace GraveyardGISApp.Data.Entities;

public partial class Note
{
    public int NoteId { get; set; }

    public int UserId { get; set; }

    public string Content { get; set; } = null!;

    public DateTime CreatedDate { get; set; }

    public int CreatedBy { get; set; }

    public DateTime ModifiedDate { get; set; }

    public int ModifiedBy { get; set; }

    public int? ContactDetailsId { get; set; }

    public int? DeceasedDetailsId { get; set; }

    public int? MaintenanceDetailsMaintId { get; set; }

    public int? PlotDetailsId { get; set; }

    public virtual Contactdetail? ContactDetails { get; set; }

    public virtual Deceaseddetail? DeceasedDetails { get; set; }

    public virtual Maintenancedetail? MaintenanceDetailsMaint { get; set; }

    public virtual Plotdetail? PlotDetails { get; set; }

    public virtual User User { get; set; } = null!;
}
