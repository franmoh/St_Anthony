using System.ComponentModel.DataAnnotations;

namespace GraveyardGFSI.Data.Entities
{
    public class Section : Auditable
    {
        [Key]
        public int SectionId { get; set; }
        public string SectionConstant { get; set; } = string.Empty;

        public Section() { }
    }
}
