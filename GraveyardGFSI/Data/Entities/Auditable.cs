namespace GraveyardGFSI.Data.Entities
{
    public abstract class Auditable : IAuditable
    {
        // Used for code reuse for things that needs a date logged when its modified.
        // Apparently abstract classes won't populate as a table in EF.
        public DateTime CreatedDate { get; set; }
        public int CreatedBy { get; set; }
        public DateTime ModifiedDate { get; set; }
        public int ModifiedBy { get; set; }
    }
}
