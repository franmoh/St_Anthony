namespace GraveyardGISApp.Data.Entities;

public partial class Plotcontactmapping
{
    public int PlotContactMappingId { get; set; }
    public int PlotDetailsId { get; set; }
    public int ContactDetailsId { get; set; }
    public bool IsPrimaryContact { get; set; }
    public DateTime CreatedDate { get; set; }
    public int CreatedBy { get; set; }
    public DateTime? ModifiedDate { get; set; }
    public int? ModifiedBy { get; set; }
}
