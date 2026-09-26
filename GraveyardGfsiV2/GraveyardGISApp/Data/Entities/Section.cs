using System;
using System.Collections.Generic;

namespace GraveyardGISApp.Data.Entities;

public partial class Section
{
    public int SectionId { get; set; }

    public string SectionConstant { get; set; } = null!;

    public DateTime CreatedDate { get; set; }

    public int CreatedBy { get; set; }

    public DateTime ModifiedDate { get; set; }

    public int ModifiedBy { get; set; }

    public virtual ICollection<Plotdetail> Plotdetails { get; set; } = new List<Plotdetail>();
}
