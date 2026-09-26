using System;
using System.Collections.Generic;

namespace GraveyardGISApp.Data.Entities;

public partial class Paymentstatus
{
    public int PaymentStatusId { get; set; }

    public string PaymentStatusConstant { get; set; } = null!;

    public DateTime CreatedDate { get; set; }

    public int CreatedBy { get; set; }

    public DateTime ModifiedDate { get; set; }

    public int ModifiedBy { get; set; }

    public virtual ICollection<Paymentdetail> Paymentdetails { get; set; } = new List<Paymentdetail>();
}
