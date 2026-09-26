namespace GraveyardGFSI.Data.Entities
{
    public interface IAuditable
    {
        // Auditable, meaning it allows the use of creating and modifying dates.
        public DateTime CreatedDate { get; set; }
        public int CreatedBy { get; set; }
        public DateTime ModifiedDate { get; set; }
        public int ModifiedBy { get; set; }
    }
}
