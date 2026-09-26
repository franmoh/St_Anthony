using System;
using System.Collections.Generic;

namespace GraveyardGISApp.Data.Entities;

public partial class Deceaseddetail
{
    public int DeceasedDetailsId { get; set; }

    public int PlotId { get; set; }

    public int ZoneId { get; set; }

    public int DeceasedStatusId { get; set; }

    public string? FirstName { get; set; }

    public string? LastName { get; set; }

    public string? MiddleName { get; set; }

    public string? Gender { get; set; }

    public DateTime? DateBuried { get; set; }

    public int? DOBYear { get; set; }

    public int? DOBMonth { get; set; }

    public int? DOBDay { get; set; }

    public int? DODYear { get; set; }

    public int? DODMonth { get; set; }

    public int? DODDay { get; set; }

    public int? NoteId { get; set; }

    public DateTime CreatedDate { get; set; }

    public int CreatedBy { get; set; }

    public DateTime? ModifiedDate { get; set; }

    public int? ModifiedBy { get; set; }

    public virtual ICollection<Note> Notes { get; set; } = new List<Note>();

    public virtual ICollection<Paymentdetail> Paymentdetails { get; set; } = new List<Paymentdetail>();
}
