namespace GraveyardGISApp.Data.Entities;

public partial class Deceasedcontactmapping
{
    public int DeceasedContactMappingId { get; set; }
    public int DeceasedDetailsId { get; set; }
    public int ContactDetailsId { get; set; }
    public bool IsPrimaryContact { get; set; }
    public string? RelationshipType { get; set; }
    public DateTime CreatedDate { get; set; }
    public int CreatedBy { get; set; }
    public DateTime? ModifiedDate { get; set; }
    public int? ModifiedBy { get; set; }
}
