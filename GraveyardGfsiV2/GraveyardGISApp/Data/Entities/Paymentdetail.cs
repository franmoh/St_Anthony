using System;
using System.Collections.Generic;

namespace GraveyardGISApp.Data.Entities;

public partial class Paymentdetail
{
    public int PaymentDetailsId { get; set; }

    public int PlotId { get; set; }

    public int? DeceasedDetailsId { get; set; }

    public int PaymentStatusId { get; set; }

    public int ContactDetailsId { get; set; }

    public int? NoteId { get; set; }

    public decimal BalancePaid { get; set; }

    public decimal BalanceDue { get; set; }

    public DateTime CreatedDate { get; set; }

    public int CreatedBy { get; set; }

    public DateTime? ModifiedDate { get; set; }

    public int? ModifiedBy { get; set; }

    public virtual Contactdetail ContactDetails { get; set; } = null!;

    public virtual Deceaseddetail? DeceasedDetails { get; set; }

    public virtual Paymentstatus PaymentStatus { get; set; } = null!;

    public virtual Plotdetail Plot { get; set; } = null!;
}
